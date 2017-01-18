from flask import Blueprint
from flask_restful import Api

from .tokens import Token
from .workouts import WorkoutList, WorkoutItem
from .users import User, Users
from .exercises import ExerciseList, Exercise

blueprint = Blueprint('api', __name__)

api = Api(blueprint)

# Add endpoints.
api.add_resource(WorkoutList, '/workouts/', endpoint="workouts")
api.add_resource(WorkoutItem, '/workouts/<id>', endpoint="workout")

api.add_resource(ExerciseList, '/exercises/', endpoint="exercises")
api.add_resource(Exercise, '/exercises/<id>', endpoint="exercise")

api.add_resource(Token, '/tokens/', endpoint="tokens")

api.add_resource(Users, '/users/', endpoint="users")
api.add_resource(User, '/users/<id>', endpoint="user")
