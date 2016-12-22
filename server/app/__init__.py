import os
from flask import Flask
from app.config import config


def create_app(config_name=None):
    """
    Creates a new Flask application and initializes application.
    """
    app = Flask(__name__)

    if config_name is None:
        config_name = os.environ.get('ENV_CONFIG', 'development')

    app.config.from_object(config[config_name])

    from app.extensions import db
    db.init_app(app)

    from app.api import blueprint as api
    app.register_blueprint(api, url_prefix='/api/1')

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    return app
