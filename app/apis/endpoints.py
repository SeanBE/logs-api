from flask_restplus import Namespace, Resource, fields

from .serializers import workout
from app.database.services import service

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

# TODO increment id???
workout = api.model('Workout', {
    'id': fields.Integer(readOnly=True, description="Unique workout identifier"),
    'username': fields.String(required=True, example="John123", description="This workout belongs to the user with this username"),
    'date_completed': fields.Date(required=True, description="Workout needs to be completed on this day"),
    'exercises': fields.List(fields.Nested(exercise), description="List of exercises for this workout")
})

@api.route('/')
# @api.doc(False)
class Workouts(Resource):

    @api.doc('list_workouts')
    @api.marshal_list_with(workout)
    def get(self):
        """
        Returns list of workouts.
        """
        # TODO not efficient.
        return list(service.all())


    @api.expect(workout)
    @api.response(201, 'Workout successfully created.')
    def post(self):
        """
        Creates a new workout.
        """
        service.create(self.api.payload)
        return None, 201


@api.route('/<username>/<date>')
# @api.doc(False)
@api.response(404, 'Workout not found')
@api.param('username', '....username workout bla')
@api.param('date', '....date workout bla')
class Workout(Resource):

    @api.doc('get_workout')
    @api.marshal_with(workout)
    @api.param('id', 'The workout identifier')
    def get(self, id):
        """
        Returns a workout.
        """
        workout = service.find(id)

        if workout:
            return workout

        api.abort(404, "Workout #{} doesn't exist".format(id))


    @api.response(204, 'Workout successfully deleted.')
    def delete(self, username, date):
        """
        Deletes a workout.
        """
        service.delete(username, date)
        return None, 204


    @api.expect(workout)
    @api.response(204, 'Workout successfully updated.')
    @api.param('id', 'The workout identifier')
    def put(self, id):
        """
        Updates a workout.
        """
        service.update(id, self.api.payload)
        return None, 204
