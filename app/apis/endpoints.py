from flask_restplus import Namespace, Resource, fields
from app.database import mongo_service as service

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
    'username': fields.String(required=True, example="John123", description="This workout belongs to the user with this username"),
    'date_proposed': fields.Date(required=True, description="Workout planned for this day"),
    'date_completed': fields.Date(description="Workout completed on this day"),
    'exercises': fields.List(fields.Nested(exercise), description="List of exercises for this workout")
})

# @api.doc(False)
@api.route('/')
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


# @api.doc(False)
@api.route('/<username>/<date>')
@api.response(404, 'Workout not found')
@api.param('username', 'Workout username')
@api.param('date', 'Workout date')
class Workout(Resource):

    @api.doc('get_workout')
    @api.marshal_with(workout)
    def get(self, username, date):
        """
        Returns a workout.
        """
        workout = service.get(username, date)

        if workout:
            return workout

        api.abort(404, "Workout for {} on {} doesn't exist".format(username, date))


    @api.response(204, 'Workout successfully deleted.')
    def delete(self, username, date):
        """
        Deletes a workout.
        """
        service.delete(username, date)
        return None, 204


    @api.expect(workout)
    @api.response(204, 'Workout successfully updated.')
    def put(self, username, date):
        """
        Updates a workout.
        """
        service.update(username, date, self.api.payload)
        return None, 204
