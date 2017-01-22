from flask import Blueprint, jsonify, make_response, current_app
from flask_restful import Api

from .tokens import Token
from .workouts import WorkoutList, WorkoutItem
from .users import User, Users
from .exercises import ExerciseList, Exercise
from .errors import HTTPException


def handle_http_exceptions(e):
    current_app.logger.info('Caught exception {}: {}'.format(e.status, e.msg))
    return make_response(jsonify(status=e.status, message=e.msg), e.status)

blueprint = Blueprint('api', __name__)
blueprint.errorhandler(HTTPException)(handle_http_exceptions)

api = Api(blueprint, catch_all_404s=False)

api.add_resource(WorkoutList, '/workouts/', endpoint="workouts")
api.add_resource(WorkoutItem, '/workouts/<id>', endpoint="workout")

api.add_resource(ExerciseList, '/exercises/', endpoint="exercises")
api.add_resource(Exercise, '/exercises/<id>', endpoint="exercise")

api.add_resource(Token, '/tokens/', endpoint="tokens")

api.add_resource(Users, '/users/', endpoint="users")
api.add_resource(User, '/users/<id>', endpoint="user")
