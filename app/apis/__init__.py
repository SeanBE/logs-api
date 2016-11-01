from flask import current_app, Blueprint
from flask_restplus import Api
from .endpoints import api as workout_api

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
    title='STRENGTH API',
    version='1.0',
    description='Lifting all the heavy shit.',
)

api.add_namespace(workout_api)
