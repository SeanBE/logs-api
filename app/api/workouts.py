from flask import request
from flask_restful import reqparse, Resource
from app.database.services import DatabaseService

Service = DatabaseService()

class Workouts(Resource):
    def get(self):
        """
        Returns list of workouts.

        Respond succesfully with 200 OK response.
        Respond with 404 Not Found if fail to fetch single resource.
        """
        # TODO not efficient.

        data, errors = Service.get_list()

        if errors:
            return None, 404

        return data , 201

    def post(self):
        """
        Creates a new workout.

        Request must include single resource object
        IF post request doesnt have client generated ID and resource created, return 201 Created Status code.
        """
        Service.create(request.get_json(force=True))
        # TODO check success of service.
        return None, 201
