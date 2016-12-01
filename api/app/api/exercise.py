from flask_restful import Resource
from app.database.services import DatabaseService


class Exercise(Resource):

    def get(self, id):
        """
        Returns a exercise.
        """
        exercise, errors = DatabaseService().get_exercise(id)

        if exercise:
            return exercise, 200

        return None, 401
