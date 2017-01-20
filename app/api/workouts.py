from flask import request, jsonify, current_app, make_response, g
from flask_restful import Resource

from webargs import fields, validate
from webargs.flaskparser import use_kwargs

from app.auth import token_auth
from app.models import Workout


class WorkoutItem(Resource):

    decorators = [token_auth.login_required]

    def get(self, id):
        """API endpoint for getting a workout

        :param id: id of workout to retrieve

        :return: status code 200 - successful retrieval
        :return: status code 404 - workout not found
        """
        workout = Workout.query.get(id)

        if workout:
            current_app.logger.info('Found workout {}'.format(id))
            return workout.dump().data, 200

        current_app.logger.info('Unable to find workout [{}]'.format(id))
        return make_response(jsonify(error="Workout not found!"), 404)

    def patch(self, id):
        """API endpoint for updating a workout

        :param id: id of workout to update

        :return: status code 404 - workout not found
        :return: status code 200 - successful update
        :return: status code 400 - unsupported Content-Type
        """
        # TODO validate data!

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
        return make_response(jsonify(error="Unsupported Content-Type!"), 400)

    def delete(self, id):
        """API endpoint for deleting a workout

        :param id: id of workout to delete

        :return: status code 204 - successful deletion
        :return: status code 404 - workout not found
        """
        workout = (Workout
                   .query
                   .get(id))

        if workout:
            error = workout.delete()
            
            if error:
                # TODO shouldn't happen..
                current_app.logger.info(
                    'Error deleting workout [{}, {}]'.format(id, error))
                return make_response(jsonify(error='Internal Server Error'), 500)

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
        """API endpoint for getting a list of workouts

        :param limit: limit number of workouts to retrieve
        :param offset: offset query from the top

        :return: status code 200 - sucessful retrieval
        """
        workout_list = (Workout
                        .query
                        .all())

        workouts, errors = Workout.dump_list(workout_list)

        if errors:
            # This should never happen...
            # TODO make this universal.
            # TODO send to sentry + log info.
            return make_response(jsonify(error='Internal Server Error'), 500)

        return workouts, 200

    def post(self):
        """API endpoint for creating a workout

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
                    current_app.logger.info('Error deserializing json to Workout [{}]'.format(json_request))
                    return make_response(jsonify(errors), 405)

                workout.user_id = g.current_user.id
                workout.save()
                current_app.logger.info('Created new workout [{}]'.format(workout.id))
                return workout.dump().data, 201

            current_app.logger.info('Invalid JSON')
            return make_response(jsonify(error="Invalid Json!"), 405)

        current_app.logger.info('Unsupported Content-Type')
        return make_response(jsonify(error="Unsupported Content-Type!"), 400)
