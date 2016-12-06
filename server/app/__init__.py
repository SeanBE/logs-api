import os
from config import config
from flask import Flask
from app.database import db

#TODO This the correct way??
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

def create_app(config_name=None):
    """
    Creates a new Flask application and initializes application.
    """
    app = Flask(__name__)

    if config_name is None:
        config_name = os.environ.get('ENV_CONFIG', 'development')

    app.config.from_object(config[config_name])

    db.init_app(app)

    from app.api import blueprint as api
    app.register_blueprint(api, url_prefix='/api/1')
    app.after_request_funcs = {None:[after_request]}

    return app
