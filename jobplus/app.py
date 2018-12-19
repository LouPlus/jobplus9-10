from flask import Flask, render_template
from jobplus.config import configs
from flask_migrate import Migrate
from flask_login import LoginManager


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    


    register_blueprints(app)
    return app


def register_blueprints(app):
    from .handlers import front
    app.register_blueprint(front)
