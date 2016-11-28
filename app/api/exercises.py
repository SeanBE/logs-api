from flask import request
from flask_restful import Resource, reqparse
from app.database.services import DatabaseService

Service = DatabaseService()
parser = reqparse.RequestParser()


class ExerciseList(Resource):

    def get(self):
        """
        Returns list of exercises.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('limit', default=10, type=int)
        parser.add_argument('offset', default=0, type=int)
        params = parser.parse_args()

        exercises, errors = Service.get_exercises(
            params['limit'], params['offset'])

        if errors:
            # TODO log errors.
            return None, 404

        for e in exercises:
            e_id = e['id']
            del e['id']
            e['_links'] = {
                "self": {
                    "href": request.url + str(e_id)
                }
            }

        return exercises, 201

    def post(self):
        """
        Creates a new exercise.
        """
        data = request.get_json(force=True)

        exercise, errors = Service.create_exercise(data)

        if errors:
            # TODO log errors.
            return None, 400

        return exercise, 201
