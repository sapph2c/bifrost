"""
Uses the application factory design pattern to create and boostrap
a Flask app instance to be used for the Bifrost C2.
"""
from flask import Flask
from flask_migrate import Migrate

import src.c2.flask_config
from src.c2.models import db
from src.c2.views.api import api
from src.c2.views.frontend import frontend


def create_app() -> Flask:
    """Creates an instance of a Flask app.

    :return: The Flask app instance
    :rtype: `Flask`
    """
    app = Flask(__name__)
    app.config.from_object(src.c2.flask_config)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app: Flask) -> None:
    """Creates and migrates the database into the Flask app instance"""
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)


def register_blueprints(app: Flask) -> None:
    """Registers blueprints contained within the views module"""
    app.register_blueprint(api)
    app.register_blueprint(frontend)
