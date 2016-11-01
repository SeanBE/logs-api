from flask import Flask
from . import config
from app.database import mongo, psql
from app.apis import blueprint as api


def create_app(config=config.BaseConfig):

    app = Flask(__name__)
    app.config.from_object(config)

    mongo.init_app(app)
    psql.init_app(app)

    app.register_blueprint(api, url_prefix='/api/1')

    return app
