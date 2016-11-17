from flask import request
from flask_restful import reqparse, Resource
from app.database.services import DatabaseService

class Workout(Resource):
    def get(self, id):
        """
        Returns a workout.
        Respond succesfully with 200 OK response.
        Respond with 404 Not Found if fail to fetch single resource.
        """
        workout = DatabaseService().get(id)

        if workout:
            return workout, 200

        return None, 401

    def patch(self, id):
        """
        Updates a workout.

        Request required single resource object (type and id).
        If missing attributes on resource, server must use current values (not null values).
        Must return 200 OK Response if update successful. Response must include updated object from GET request.
        Return 404 Not Found when resource does not exist.
        """
        # TODO request.json
        data, errors = DatabaseService().update(id, request.get_json(force=True))

        if errors:
            return errors, 401

        return data, 200

    def delete(self, id):
        """
        Deletes a workout.

        Return 204 No Content Status Code if successful. 
        """
        errors = DatabaseService().delete(id)

        if errors:
            return errors, 401

        return None, 204
