"""
Blueprint that contains all of the frontend endpoints seen by
the users of Bifrost.
"""

import subprocess
from datetime import datetime, timedelta
from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import StringField
from wtforms.fields.simple import PasswordField

from src.c2.models import Agent, User, db

frontend = Blueprint("frontend", __name__)


def login_required(f):
    """Requires a user to login before they can access critical endpoints

    :returns: redirects an unauthenticated user to /login
    :rtype: wrap
    """

    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        flash("You need to login first.")
        return redirect(url_for("frontend.login"))

    return wrap


@frontend.route("/signup", methods=["GET", "POST"])
def signup():
    """Endpoint that allows a user to register an account"""
    form = UserRegistration()

    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        already_user = User.query.filter_by(email=email).first()

        if already_user:
            return f"{username} is already registered."

        new_user = User(email, username, password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("frontend.login"))

    return render_template("signup.html", form=form)


class UserRegistration(FlaskForm):
    email = StringField("email")
    username = StringField("username")
    password = PasswordField("password")


@frontend.route("/login", methods=["GET", "POST"])
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
            return redirect(url_for("frontend.home"))
        error = "Invalid username or password"
    return render_template("login.html", error=error)


class UserLogin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def attempt_login(self):
        actual_user = User.query.filter(User.username == self.username).first()
        if not actual_user:
            return False
        if not check_password_hash(actual_user.password, self.password):
            return False
        return True


@frontend.route("/", methods=["GET"])
@login_required
def home():
    """Endpoint that displays a pwnboard that includes all of the
    active agents calling back to the server

    """
    check_agents_statuses()
    agents = db.session.query(Agent).all()
    return render_template("index.html", agents=agents)


def check_agents_statuses() -> None:
    """Function that checks if an agent is still alive
    using its sleep time along with the last time it checked in

    """
    agents = db.session.query(Agent).all()
    for agent in agents:
        last_seen = agent.last_seen
        last_seen = datetime.strptime(last_seen, "%d %B, %Y %H:%M:%S")
        curr_time = datetime.now()
        elapsed = curr_time - last_seen
        expected_check_in_time = timedelta(seconds=(agent.sleep_time * 2 + 10))
        if elapsed > expected_check_in_time:
            agent.is_alive = False
        else:
            agent.is_alive = True
        db.session.flush()
        db.session.commit()


@frontend.route("/config", methods=["GET", "POST"])
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


def build_agent(ip: str = "127.0.0.1", sleeptime: str = "0") -> None:
    """Builds the binary using the user provided config values

    :param ip: The callback IP address, defaulted at localhost
    :type ip: str
    :param sleeptime: The amount of time the agent should wait to callback
    :type sleeptime: str
    :returns: none
    :rtype: None
    """
    subprocess.Popen([f"/Bifrost/src/agent/make.sh -h {ip} -s {sleeptime}"], shell=True)


class AgentConfig(FlaskForm):
    callback_ip = StringField("Callback IP")
    sleep = StringField("Sleep Time")


@frontend.route("/agent<agent_id>", methods=["GET"])
@login_required
def display_agent(agent_id):
    """Endpoint that displays all the information regarding the
    agent with the specified ID, and includes an interactive shell.

    :param id: The ID of the agent
    :type id: str
    """
    selected_agent = Agent.query.filter_by(id=agent_id).first()
    return render_template("agent.html", agent=selected_agent)


@frontend.route("/logout", methods=["GET"])
@login_required
def logout():
    """Endpoint that allows a user to logout of their session"""
    session.pop("logged_in", None)
    flash("You were just logged out!")
    return redirect(url_for("frontend.login"))
