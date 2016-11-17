from . import config
from flask import Flask

from app.database import db
from app.api import blueprint as api


def create_app(config=config.DevConfig):
    """
    Creates a new Flask application and initializes application.
    """

    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    app.register_blueprint(api, url_prefix='/api/1')

    return app
