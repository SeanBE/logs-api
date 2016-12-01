from flask import Blueprint
from flask_restful import Api
from .workouts import WorkoutList
from .exercises import ExerciseList
from .exercise import Exercise
from .workout import Workout

blueprint = Blueprint('api', __name__)

api = Api(blueprint)
api.add_resource(WorkoutList, '/workouts/')
api.add_resource(ExerciseList, '/exercises/')
api.add_resource(Exercise, '/exercises/<id>')
api.add_resource(Workout, '/workouts/<id>')
