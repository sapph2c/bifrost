from app import db


class Agent(db.Model):
    __tablename__ = "AGENTS"
    id = db.Column(db.Integer, primary_key=True)
    os = db.Column(db.String, nullable=False)
    host_name = db.Column(db.String, nullable=True)
    ip = db.Column(db.String, nullable=True)
    ram = db.Column(db.String, nullable=True)

    def __init__(self, os, host_name, ip, ram):
        self.os = os
        self.host_name = host_name
        self.ip = ip
        self.ram = ram

    def __repr__(self):
        return f"title: {self.title}, description: {self.description}"
