from . import config
from flask import Flask

from app.database import db
from app.api import blueprint as api

#TODO This the correct way??
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

def create_app(config=config.DevConfig):
    """
    Creates a new Flask application and initializes application.
    """
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    app.register_blueprint(api, url_prefix='/api/1')
    app.after_request_funcs = {None:[after_request]}

    return app
