from flask import request
from flask_restful import Resource, reqparse

from app.auth import auth
from app.database.models import Workout as W


class Workout(Resource):

    decorators = [auth.login_required]

    def get(self, id):

        workout = W.query.filter_by(id=id).first()

        if workout:
            data, errors = workout.dump()
            return data, 201

        return None, 401

    def patch(self, id):

        data = request.get_json(force=True)
        workout = W.query.filter_by(id=id).first()
        result = workout.update(data)
        # TODO what is result?
        # if errors:
        #     return errors, 404

        return result, 200

    def delete(self, id):

        workout = W.query.filter_by(id=id).first()
        deleted = workout.delete()

        if deleted:
            return None, 204

        return None, 404


class WorkoutList(Resource):

    decorators = [auth.login_required]

    def get(self):
        """
        Returns list of workouts.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('limit', default=10, type=int)
        parser.add_argument('offset', default=0, type=int)
        p = parser.parse_args()

        result = W.query.limit(p['limit']).offset(p['offset']).all()
        workouts, errors = W.dump_list(result)

        if errors:
            return None, 401

        return workouts, 201

    def post(self):
        """
        Creates a new workout.
        """
        # force=True (the mimetype is ignored).
        data = request.get_json(force=True)

        workout = W.load(data)
        workout.save()

        return workout.dump(), 201
