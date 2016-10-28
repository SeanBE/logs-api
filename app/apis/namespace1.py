from flask import current_app
from flask_restplus import Namespace, Resource, fields
from .serializers import workout
from app.database import db as mongo

api = Namespace('workouts', description='Workout operations')

exercise_set = api.model('Set', {
    "reps": fields.Integer(required=True, example=10, description="Repetitions required to complete set"),
    "weight": fields.Integer(example=120, default=-1, description="Weight to be used for each repetition"),
    "comment": fields.String(example="Easy set!", default="", description="Comments about this set")
})

exercise = api.model('Exercise', {
    'name': fields.String(required=True, example="Bench Press"),
    'sets': fields.List(fields.Nested(exercise_set), required=True, description="List of sets required to be completed with this exercise")
})

workout = api.model('Workout', {
    'id': fields.Integer(readOnly=True, description="Unique workout identifier"),
    'username': fields.String(required=True, example="John123", description="This workout belongs to the user with this username"),
    'date_completed': fields.Date(required=True, description="Workout needs to be completed on this day"),
    'exercises': fields.List(fields.Nested(exercise), description="List of exercises for this workout")
})

@api.route('/')
class Workouts(Resource):
    @api.doc('list_workouts')
    @api.marshal_list_with(workout)
    def get(self):
        return mongo.db.workouts.find()

    @api.doc(False)
    @api.expect(workout)
    @api.marshal_with(workout, code=201)
    def post(self):
        return mongo.db.workouts.insert_one(request.json), 201


@api.route('/<int:id>')
@api.response(404, 'Workout not found')
@api.param('id', 'The workout identifier')
class Workout(Resource):
    @api.doc('get_workout')
    @api.marshal_with(workout)
    def get(self, id):
        '''Fetch a given resource'''
        return mongo.db.workouts.find_one({'id': id})


    @api.doc(False)
    @api.response(204, 'Workout deleted')
    def delete(self, id):
        mongo.db.workouts.delete_one({'id':id})
        return '', 204

    @api.doc(False)
    @api.expect(workout)
    @api.marshal_with(workout)
    def put(self, id):
        return mongo.db.workouts.replace_one({'id': id}, request.json)
