from flask import Blueprint
from flask_restful import Api
from .workouts import WorkoutList
from .workout import Workout

blueprint = Blueprint('api', __name__)

api = Api(blueprint)
api.add_resource(WorkoutList, '/workouts/')
api.add_resource(Workout, '/workouts/<id>')

#TODO authentication
# https://github.com/miguelgrinberg/flask-httpauth
# https://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful/page/0
