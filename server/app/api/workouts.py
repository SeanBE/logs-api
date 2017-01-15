from flask import request, jsonify, current_app, make_response
from flask_restful import Resource

from webargs import fields, validate
from webargs.flaskparser import use_kwargs

from app.auth import token_auth
from app.models import Workout as W
from app.models.workout import WorkoutSchema


class Workout(Resource):

    decorators = [token_auth.login_required]

    def get(self, id):

        workout = W.query.get(id)

        if workout:
            current_app.logger.debug('Found workout {}'.format(workout.id))
            return workout.dump().data, 200

        return make_response(jsonify(error="Workout not found!"), 404)

    def patch(self, id):
        # content type needs to be application/json.
        data = request.get_json(silent=True)
        if data:
            workout = W.query.get(id)
            if workout:
                workout.update(**data)
                return workout.dump().data, 200

            return make_response(jsonify(error="Workout not found!"), 404)
        return make_response(jsonify(error="No data provided!"), 400)

    def delete(self, id):

        workout = (W
                   .query
                   .get(id))

        if workout:
            # TODO delete currently returns None?? why?
            workout.delete()
            current_app.logger.debug('Deleted workout {}'.format(workout.id))
            return None, 204

        current_app.logger.debug('Could not find workout (id {})'.format(id))
        return make_response(jsonify(error="Could not delete workout!"), 404)


class WorkoutList(Resource):

    decorators = [token_auth.login_required]

    page_args = {
        'limit': fields.Int(missing=5),
        'offset': fields.Int(missing=0)
    }

    @use_kwargs(page_args)
    def get(self, limit, offset):

        workout_list = (W
                        .query
                        # .limit(limit)
                        # .offset(offset)
                        .all())

        workouts, errors = W.dump_list(workout_list)

        return workouts, 200

    def post(self):

        data = request.get_json(force=True)
        workout, errors = W.load(data)
        # TODO if errors do not save!!
        workout.save()

        return workout.dump().data, 201
