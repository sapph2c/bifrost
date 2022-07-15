from flask import Flask
from flask_migrate import Migrate

import c2.flask_config
from c2.models import db
from c2.views.api import api
from c2.views.frontend import frontend


def create_app():
    app = Flask(__name__)
    app.config.from_object(c2.flask_config)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(api)
    app.register_blueprint(frontend)
