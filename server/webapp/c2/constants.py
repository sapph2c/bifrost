from flask.app import Flask
from flask.blueprints import Blueprint
from flask_sqlalchemy import SQLAlchemy

from config import BaseConfig

app = Flask(__name__)
# set database name
app.database = "agents.db"
# load the config
app.config.from_object(BaseConfig)
api = Blueprint('api', __name__)
app.register_blueprint(api)
# create the sqlalchemy object
