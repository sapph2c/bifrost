from config import BaseConfig
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# set database name
app.database = "agents.db"
# load the config
app.config.from_object(BaseConfig)
# create the sqlalchemy object
db = SQLAlchemy(app)


class Agent(db.Model):
    """Class that holds agent information in an AGENTS table

    """
    __tablename__ = "AGENTS"
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String, nullable=False)
    uptime = db.Column(db.String, nullable=True)
    bootTime = db.Column(db.String, nullable=True)
    procs = db.Column(db.String, nullable=True)
    os = db.Column(db.String, nullable=True)
    platform = db.Column(db.String, nullable=True)
    platformFamily = db.Column(db.String, nullable=True)
    platformVersion = db.Column(db.String, nullable=True)
    kernelVersion = db.Column(db.String, nullable=True)
    kernelArch = db.Column(db.String, nullable=True)
    virtualizationSystem = db.Column(db.String, nullable=True)
    virtualizationRole = db.Column(db.String, nullable=True)
    hostID = db.Column(db.String, nullable=True)
    ram = db.Column(db.String, nullable=True)
    ip = db.Column(db.String, nullable=True)
    username = db.Column(db.String, nullable=True)
    isAlive = db.Column(db.Boolean, nullable=True)
    lastSeen = db.Column(db.String, nullable=True)
    sleepTime = db.Column(db.Integer, nullable=True)

    def __init__(self, hostname, uptime, bootTime, procs, os, platform,
                 platformFamily, platformVersion, kernelVersion,
                 kernelArch, virtualizationSystem,
                 virtualizationRole, hostID, ram, ip, username, sleepTime):
        self.hostname = hostname
        self.uptime = uptime
        self.bootTime = bootTime
        self.procs = procs
        self.os = os
        self.platform = platform
        self.platformFamily = platformFamily
        self.platformVersion = platformVersion
        self.kernelVersion = kernelVersion
        self.kernelArch = kernelArch
        self.virtualizationSystem = virtualizationSystem
        self.virtualizationRole = virtualizationRole
        self.hostID = hostID
        self.ram = ram
        self.ip = ip
        self.username = username
        self.isAlive = True
        self.lastSeen = "0"
        self.sleepTime = sleepTime


class Commands(db.Model):
    """Class that holds command information in a COMMANDS table
    """
    __tablename__ = "COMMANDS"
    commandID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    implantID = db.Column(db.String, nullable=False)
    command = db.Column(db.String, nullable=True)
    output = db.Column(db.String, nullable=True)
    retrieved = db.Column(db.String, nullable=True)
    displayed = db.Column(db.String, nullable=True)

    def __init__(self, implantID, command=None,
                 output=None, retrieved=False, displayed=False):
        self.implantID = implantID
        self.command = command
        self.output = output
        self.retrieved = retrieved
        self.displayed = displayed
