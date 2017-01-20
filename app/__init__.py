import os
import logging
from flask import Flask, jsonify, make_response
from app.config import config


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        config_name = os.environ.get('ENV_CONFIG', 'development')

    app.config.from_object(config[config_name])

    if not app.debug:
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)

    app.logger.info('Application running in {} mode (DEBUG IS {})'.format(config_name, str(app.debug)))

    # Import and init extensions
    from app.extensions import db, sentry

    db.init_app(app)

    if config_name is 'production':
        sentry.init_app(app, logging=True, level=logging.INFO)

    # Import and register blueprints
    from app.api import blueprint as api
    app.register_blueprint(api, url_prefix='/1')

    @app.errorhandler(404)
    def page_not_found(e):
        return make_response(jsonify(error=str(e)), 400)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'content-type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PUT,POST,PATCH,DELETE')
        return response

    return app
