import os
import logging
from flask import Flask, jsonify
from app.config import config


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        config_name = os.environ.get('ENV_CONFIG', 'development')

    app.config.from_object(config[config_name])

    configure_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)

    app.logger.info('Application running in {} mode (DEBUG IS {})'.format(config_name, str(app.debug)))

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'content-type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PUT,POST,PATCH,DELETE')
        return response

    return app


def configure_logging(app):
    if not app.debug:
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)


def register_errorhandlers(app):
    def page_not_found(e):
        return (jsonify(message='Page Not Found', status=404), 404)
    app.errorhandler(404)(page_not_found)


def register_blueprints(app):
    from app.api import blueprint as api

    app.register_blueprint(api, url_prefix='/1')


def register_extensions(app):
    from app.extensions import db, sentry

    db.init_app(app)
    if app.config['ENV'] is 'production':
        sentry.init_app(app, logging=True, level=logging.INFO)
