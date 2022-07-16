from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class Agent(db.Model):
    """Class that holds agent information in an AGENTS table"""

    __tablename__ = "AGENTS"
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String, nullable=False)
    os = db.Column(db.String, nullable=True)
    username = db.Column(db.String, nullable=True)
    ip = db.Column(db.String, nullable=False)
    is_alive = db.Column(db.Boolean, nullable=True)
    last_seen = db.Column(db.String, nullable=True)
    sleep_time = db.Column(db.Integer, nullable=True)

    def __init__(
        self,
        hostname,
        os,
        username,
        ip,
        sleep_time,
    ):
        self.hostname = hostname
        self.os = os
        self.username = username
        self.ip = ip
        self.is_alive = True
        self.sleep_time = sleep_time
        self.last_seen = "0"


class Command(db.Model):
    """Class that holds command information in a COMMANDS table"""

    __tablename__ = "COMMANDS"
    command_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    agent_id = db.Column(db.String, nullable=False)
    command = db.Column(db.String, nullable=True)
    output = db.Column(db.String, nullable=True)
    retrieved = db.Column(db.String, nullable=True)
    displayed = db.Column(db.String, nullable=True)

    def __init__(
        self, agent_id, command=None, output=None, retrieved=False, displayed=False
    ):
        self.agent_id = agent_id
        self.command = command
        self.output = output
        self.retrieved = retrieved
        self.displayed = displayed


class User(db.Model):
    """Class that holds an authenticated user"""

    __tablename__ = "USERS"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True)
    """TODO
    Make sure password is hashed to protect data at rest 
    """
    username = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password, method="sha256")
