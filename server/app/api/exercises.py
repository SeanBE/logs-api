from flask import request, jsonify, make_response, current_app
from flask_restful import Resource

from webargs import fields, validate
from webargs.flaskparser import use_kwargs

from app.auth import token_auth
from app.models import Exercise as Ex


class Exercise(Resource):

    decorators = [token_auth.login_required]

    def get(self, id):

        exercise = Ex.query.get(id)

        if exercise:
            return exercise.dump().data, 200

        return make_response(jsonify(error="Exercise not found!"), 404)

    def patch(self, id):
        # content type needs to be application/json.
        data = request.get_json(silent=True)
        if data:
            exercise = Ex.query.get(id)
            if exercise:
                exercise.update(**data)
                return exercise.dump().data, 200
            return make_response(jsonify(error="Exercise not found!"), 404)

        return make_response(jsonify(error="No data provided!"), 400)


    def delete(self, id):

        exercise = (Ex
                    .query
                    .get(id))

        if exercise:
            error = exercise.delete()
            if error:
                current_app.logger.debug('Error deleting {}'.format(exercise.id))
                # TODO what do we do?
                return make_response(jsonify(error="Could not delete exercise!"), 404)

            return None, 204

        current_app.logger.debug('Could not find exercise (id {})'.format(id))
        return make_response(jsonify(error="Could not delete exercise!"), 404)


class ExerciseList(Resource):

    decorators = [token_auth.login_required]

    page_args = {
        'limit': fields.Int(missing=10),
        'offset': fields.Int(missing=0)
    }

    @use_kwargs(page_args)
    def get(self, limit, offset):

        exercises_result = (Ex
                            .query
                            .all())

        exercises, errors = Ex.dump_list(exercises_result)

        return exercises, 200

    def post(self):

        data = request.get_json(force=True)
        exercise, errors = Ex.load(data)
        exercise.save()
        return exercise.dump().data, 201
