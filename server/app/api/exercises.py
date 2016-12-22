from flask import request
from flask_restful import Resource

from webargs import fields, validate
from webargs.flaskparser import use_kwargs

from app.auth import auth
from app.models import Exercise as Ex


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

    page_args = {
        'limit': fields.Int(missing=10),
        'offset': fields.Int(missing=0)
    }

    @use_kwargs(page_args)
    def get(self, limit, offset):

        exercises_result = (Ex
                            .query
                            .limit(limit)
                            .offset(offset)
                            .all())

        exercises, errors = Ex.dump_list(exercises_result)

        return exercises, 200

    def post(self):

        data = request.get_json(force=True)
        exercise = Ex.load(data).save()

        return exercise.dump().data, 201
