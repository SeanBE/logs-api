from flask import request
from flask_restful import Resource, reqparse
from app.database.services import DatabaseService

Service = DatabaseService()

parser = reqparse.RequestParser()

class WorkoutList(Resource):
    def get(self):
        """
        Returns list of workouts.

        Respond succesfully with 200 OK response.
        Respond with 404 Not Found if fail to fetch single resource.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('limit', default=10, type=int)
        parser.add_argument('offset', default=0, type=int)
        params = parser.parse_args()

        data, errors = Service.get_list(params['limit'], params['offset'])

        if errors:
            return None, 404

        return data , 201

    def post(self):
        """
        Creates a new workout.

        Request must include single resource object
        If post request doesnt have client generated ID and resource created, return 201 Created Status code.
        """
        # TODO check success of service.
        # force=True why?
        Service.create(request.get_json(force=True))
        return None, 201
