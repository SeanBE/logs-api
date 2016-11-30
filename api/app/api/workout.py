from flask import request
from flask_restful import reqparse, Resource
from app.database.services import DatabaseService


class Workout(Resource):

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
