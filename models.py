# create the application object
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import BaseConfig

app = Flask(__name__)
# set database name
app.database = "agents.db"
# load the config
app.config.from_object(BaseConfig)
# create the sqlalchemy object
db = SQLAlchemy(app)


class Agent(db.Model):
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

    def __init__(self, hostname, uptime, bootTime, procs, os, platform, platformFamily, platformVersion, kernelVersion, kernelArch, virtualizationSystem, virtualizationRole, hostID, ram, ip):
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

    def __repr__(self):
        return f"os: {self.os}, host_name: {self.hostname}, ip: {self.ip}, ram: {self.ram}, id: {self.id}"


class CommandQueue(db.Model):
    __tablename__ = "COMMAND QUEUE"
    id = db.Column(db.String, primary_key=True)
    command = db.Column(db.String, nullable=True)
    output = db.Column(db.String, nullable=True)

    def __init__(self, id, command=None, output=None):
        self.id = id
        self.command = command
        self.output = output

    def __repr__(self):
        return f"id: {self.id}, command: {self.command}, output: {self.output}"
