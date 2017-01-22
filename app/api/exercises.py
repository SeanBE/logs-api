from flask import request, jsonify, make_response, current_app
from flask_restful import Resource

from webargs import fields, validate
from webargs.flaskparser import use_kwargs

from app.auth import token_auth
from app.models import Exercise as Ex

from .errors import ResourceDoesNotExist


class Exercise(Resource):

    decorators = [token_auth.login_required]

    def get(self, id):
        """API endpoint for getting an exercise

        :param id: id of exercise to retrieve

        :return: status code 200 - successful retrieval
        :return: status code 404 - exercise not found
        """

        exercise = Ex.query.get(id)

        if exercise:
            current_app.logger.info(
                'Found exercise {}.'.format(id))

            return exercise.dump().data, 200

        raise ResourceDoesNotExist(
            'Exercise with ID [{}] does not exist.'.format(id))

    def patch(self, id):
        """API endpoint for updating an exercise

        :param id: id of exercise to update

        :return: status code 404 - exercise not found
        :return: status code 200 - successful update
        :return: status code 400 - unsupported Content-Type
        """
        # TODO validate data!

        # content type needs to be application/json.
        data = request.get_json(silent=True)
        if data:
            exercise = Ex.query.get(id)
            if exercise:
                exercise.update(**data)
                current_app.logger.info('Updated exercise [{}].'.format(id))
                return exercise.dump().data, 200

            raise ResourceDoesNotExist(
                'Exercise with ID [{}] does not exist.'.format(id))

        current_app.logger.info('Content-type not accepted.')
        return make_response(jsonify(error="No data provided!"), 400)

    def delete(self, id):
        """API endpoint for deleting an exercise

        :param id: id of exercise to delete

        :return: status code 204 - successful deletion
        :return: status code 404 - exercise not found
        """
        exercise = (Ex
                    .query
                    .get(id))

        if exercise:
            error = exercise.delete()

            if error:
                # TODO shouldn't happen..
                current_app.logger.info(
                    'Error deleting exercise [{}, {}]'.format(id, error))
                return make_response(jsonify(error='Internal Server Error'), 500)

            current_app.logger.info('Deleted exercise [{}]'.format(id))
            return None, 204

        raise ResourceDoesNotExist(
            'Exercise with ID [{}] does not exist.'.format(id))


class ExerciseList(Resource):

    decorators = [token_auth.login_required]

    page_args = {
        'limit': fields.Int(missing=10),
        'offset': fields.Int(missing=0)
    }

    @use_kwargs(page_args)
    def get(self, limit, offset):
        """API endpoint for getting a list of exercises

        :param limit: limit number of exercises to retrieve
        :param offset: offset query from the top

        :return: status code 200 - sucessful retrieval
        """

        exercise_list = (Ex
                         .query
                         .all())

        exercises, errors = Ex.dump_list(exercise_list)

        if errors:
            # This should never happen...
            # TODO make this universal.
            # TODO send to sentry + log info.
            return make_response(jsonify(error='Internal Server Error'), 500)

        return exercises, 200

    def post(self):
        """API endpoint for creating an exercise

        :return: status code 405 - invalid JSON or invalid request type
        :return: status code 400 - unsupported Content-Type
        :return: status code 201 - successful submission
        """

        # Ensure post's Content-Type is supported
        if request.is_json:
            # Ensure data is a valid JSON
            json_request = request.get_json(silent=True)

            if json_request:
                exercise, errors = Ex.load(json_request)

                if errors:
                    current_app.logger.info(
                        'Error deserializing json to Exercise [{}]'.format(json_request))
                    return make_response(jsonify(errors), 405)

                exercise.save()
                current_app.logger.info(
                    'Created new exercise [{}]'.format(exercise.id))
                return exercise.dump().data, 201

            current_app.logger.info('Invalid JSON')
            return make_response(jsonify(error="Invalid JSON!"), 405)

        current_app.logger.info('Unsupported Content-Type')
        return make_response(jsonify(error="Unsupported Content-Type!"), 400)
