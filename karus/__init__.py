from .api import api_blueprint
from .home import home_blueprint
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_blueprint)
    app.register_blueprint(home_blueprint)

    return app
