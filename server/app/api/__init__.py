from flask import Blueprint
from flask_restful import Api

from .tokens import Token
from .workouts import WorkoutList, Workout
from .users import User, Users
from .exercises import ExerciseList, Exercise

blueprint = Blueprint('api', __name__)

api = Api(blueprint)

# Add endpoints.
api.add_resource(WorkoutList, '/workouts/')
api.add_resource(Workout, '/workouts/<id>')

api.add_resource(ExerciseList, '/exercises/')
api.add_resource(Exercise, '/exercises/<id>')

api.add_resource(Token, '/tokens/')

api.add_resource(Users, '/users/')
api.add_resource(User, '/users/<id>')
