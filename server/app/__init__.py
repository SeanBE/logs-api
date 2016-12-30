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

    if not app.debug:
        import logging
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)

    # Import and init extensions
    from app.extensions import db, sentry
    db.init_app(app)
    sentry.init_app(app, logging=True, level=logging.INFO)

    # Import and register blueprints
    from app.api import blueprint as api
    app.register_blueprint(api, url_prefix='/api/1')

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'content-type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    return app
