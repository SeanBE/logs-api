from flask import request
from flask_restful import Resource

from webargs import fields, validate
from webargs.flaskparser import use_kwargs

from app.auth import auth
from app.models import Workout as W


class Workout(Resource):

    decorators = [auth.login_required]

    def get(self, id):

        workout = W.query.filter_by(id=id).first()

        if workout:
            return workout.dump().data, 200

        return {"error": "Workout not found!"}, 404

    def patch(self, id):
        data = request.get_json(force=True)
        workout = W.query.filter_by(id=id).first()

        workout.update(**data)
        return workout.dump().data, 200

    def delete(self, id):

        deleted = (W
                   .query
                   .filter_by(id=id)
                   .first()
                   .delete())

        if deleted:
            return None, 204

        return {"error": "Could not delete workout!"}, 404


class WorkoutList(Resource):

    decorators = [auth.login_required]

    page_args = {
        'limit': fields.Int(missing=5),
        'offset': fields.Int(missing=0)
    }

    @use_kwargs(page_args)
    def get(self, limit, offset):

        workout_list = (W
                        .query
                        .limit(limit)
                        .offset(offset)
                        .all())

        workouts, errors = W.dump_list(workout_list)

        return workouts, 200

    def post(self):

        data = request.get_json(force=True)
        workout = W.load(data).save()

        return workout.dump().data, 201
