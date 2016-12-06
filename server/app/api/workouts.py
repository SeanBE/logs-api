from flask import request
from flask_restful import Resource, reqparse

from app.auth import auth
from app.database.services import DatabaseService

Service = DatabaseService()
parser = reqparse.RequestParser()


class Workout(Resource):

    decorators = [auth.login_required]

    def get(self, id):
        """
        Returns a workout.
        """
        workout = DatabaseService().get(id)

        if workout:
            return workout, 200

        return None, 401

    def patch(self, id):
        """
        Updates a workout.
        """
        data, errors = DatabaseService().update(id, request.get_json(force=True))

        if errors:
            return errors, 404

        return data, 200

    def delete(self, id):
        """
        Deletes a workout.
        """
        errors = DatabaseService().delete(id)

        if errors:
            return errors, 404

        return None, 204


class WorkoutList(Resource):

    decorators = [auth.login_required]

    def get(self):
        """
        Returns list of workouts.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('limit', default=10, type=int)
        parser.add_argument('offset', default=0, type=int)
        params = parser.parse_args()

        workouts, errors = Service.get_list(params['limit'], params['offset'])

        if errors:
            # TODO log errors.
            return None, 404

        return workouts, 201

    def post(self):
        """
        Creates a new workout.
        """
        # force=True (the mimetype is ignored).
        data = request.get_json(force=True)

        workout, errors = Service.create(data)

        if errors:
            # TODO log errors.
            return None, 400

        return workout, 201
