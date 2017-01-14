import os
import logging
from flask import Flask, jsonify
from app.config import config


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        config_name = os.environ.get('ENV_CONFIG', 'development')

    app.config.from_object(config[config_name])

    if not app.debug:
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.DEBUG)

    # Import and init extensions
    from app.extensions import db, sentry

    db.init_app(app)

    # TODO If production config.
    # sentry.init_app(app, logging=True, level=logging.INFO)

    # Import and register blueprints
    from app.api import blueprint as api
    app.register_blueprint(api, url_prefix='/1')

    # TODO right way?
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify(error=404, text=str(e)), 404

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'content-type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PUT,POST,PATCH,DELETE')
        return response

    return app
