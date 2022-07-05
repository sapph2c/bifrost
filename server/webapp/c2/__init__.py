from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# set database name
app.database = "agents.db"
# load the config
app.config["DEBUG"] = False
app.config[
    "SECRET_KEY"
] = "\x8d1K\x1f\x17\xd5\xbbU\xbc\xd3\xc3n\xfd,umH\x1b\xe9\
4Wc\x90"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///agents.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# create the sqlalchemy object
db = SQLAlchemy(app)

from c2.models import Agent, Command

db.create_all()
db.session.commit()

from c2.api.bot_communication import app, bp

app.register_blueprint(bp)
