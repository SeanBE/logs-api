from flask import request, jsonify, current_app, make_response, g
from flask_restful import Resource

from webargs import fields, validate
from webargs.flaskparser import use_kwargs

from app.auth import token_auth
from app.models import Workout
from app.models.workout import WorkoutSchema


class WorkoutItem(Resource):

    decorators = [token_auth.login_required]

    def get(self, id):
        workout = Workout.query.get(id)

        if workout:
            current_app.logger.info('Found workout {}'.format(id))
            return workout.dump().data, 200

        current_app.logger.info('Unable to find workout [{}]'.format(id))
        return make_response(jsonify(error="Workout not found!"), 404)

    def patch(self, id):
        # content type needs to be application/json.
        data = request.get_json(silent=True)
        if data:
            workout = Workout.query.get(id)
            if workout:
                workout.update(**data)
                current_app.logger.info('Updated workout [{}]'.format(id))
                return workout.dump().data, 200

            current_app.logger.info('Unable to find workout [{}]'.format(id))
            return make_response(jsonify(error="Workout not found!"), 404)

        current_app.logger.info('Content-type not accepted')
        return make_response(jsonify(error="No data provided!"), 400)

    def delete(self, id):

        workout = (Workout
                   .query
                   .get(id))

        if workout:
            workout.delete()
            current_app.logger.info('Deleted workout {}'.format(id))
            return None, 204

        current_app.logger.info('Could not find workout [{}]'.format(id))
        return make_response(jsonify(error="Could not delete workout!"), 404)


class WorkoutList(Resource):

    decorators = [token_auth.login_required]

    page_args = {
        'limit': fields.Int(missing=5),
        'offset': fields.Int(missing=0)
    }

    @use_kwargs(page_args)
    def get(self, limit, offset):

        workout_list = (Workout
                        .query
                        .all())

        workouts, errors = Workout.dump_list(workout_list)

        return workouts, 200

    def post(self):
        """API endpoint for creating a workout.

        :return: status code 405 - invalid JSON or invalid request type
        :return: status code 400 - unsupported Content-Type
        :return: status code 201 - successful submission
        """

        # Ensure post's Content-Type is supported
        if request.is_json:
            # Ensure data is a valid JSON
            json_request = request.get_json(silent=True)

            if json_request:
                workout, errors = Workout.load(json_request)

                if errors:
                    return make_response(jsonify(errors), 405)
                workout.user_id = g.current_user.id
                workout.save()
                current_app.logger.info('Created new workout [{}]'.format(id))
                return workout.dump().data, 201

            current_app.logger.info('Invalid JSON')
            return make_response(jsonify(error="Invalid Json!"), 405)

        current_app.logger.info('Unsupported Content-Type')
        return make_response(jsonify(error="Unsupported Content-Type!"), 400)
