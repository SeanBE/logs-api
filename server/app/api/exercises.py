from flask import request
from flask_restful import Resource, reqparse
from app.auth import auth
from app.database.models import Exercise as Ex


class Exercise(Resource):

    decorators = [auth.login_required]

    def get(self, id):

        exercise = Ex.query.filter_by(id=id).first()

        if exercise:
            return exercise.dump().data, 200

        return {"error": "Exercise not found!"}, 404

    def patch(self, id):
        data = request.get_json(force=True)
        exercise = Ex.query.filter_by(id=id).first()

        exercise.update(**data)
        return exercise.dump().data, 200

    def delete(self, id):

        deleted = (Ex
                   .query
                   .filter_by(id=id)
                   .first()
                   .delete())

        if deleted:
            return None, 204

        return {"error": "Could not delete exercise!"}, 404


class ExerciseList(Resource):

    decorators = [auth.login_required]

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('limit', default=10, type=int)
        parser.add_argument('offset', default=0, type=int)
        p = parser.parse_args()

        exercises_result = (Ex
                            .query
                            .limit(p['limit'])
                            .offset(p['offset'])
                            .all())

        exercises, errors = Ex.dump_list(exercises_result)

        return exercises, 200

    def post(self):

        data = request.get_json(force=True)
        exercise = Ex.load(data).save()

        return exercise.dump().data, 201
