from flask import request
from flask_restful import Resource, reqparse

from app.auth import auth
from app.database.models import Exercise as ExerciseModel

parser = reqparse.RequestParser()

class Exercise(Resource):

    decorators = [auth.login_required]

    def get(self, id):
        """
        Returns a exercise.
        """
        exercise = ExerciseModel.query.filter_by(id=id).first()

        if exercise:
            return {'name': exercise.name, 'id': exercise.id}, 200

        return None, 401


class ExerciseList(Resource):

    decorators = [auth.login_required]

    def get(self):
        """
        Returns list of exercises.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('limit', default=10, type=int)
        parser.add_argument('offset', default=0, type=int)
        params = parser.parse_args()

        exercises_result = (ExerciseModel
                            .query
                            .limit(params['limit'])
                            .offset(params['offset'])
                            .all())

        exercises = [{'name': e.name, 'id': e.id} for e in exercises_result]

        # TODO nasty.
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

        exercise = ExerciseModel(data['name'])

        db.session.add(exercise)
        db.session.commit()

        # TODO try catch?
        # if errors:
        # return None, 400

        return exercise, 201
