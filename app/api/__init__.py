from flask import Blueprint
from flask_restful import Api
from .workouts import Workouts
from .workout import Workout

blueprint = Blueprint('api', __name__)

api = Api(blueprint)
api.add_resource(Workouts, '/workouts/')
api.add_resource(Workout, '/workouts/<id>')
