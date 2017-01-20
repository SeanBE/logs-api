from flask import g, request, jsonify, abort, make_response, current_app
from flask_restful import Resource

from app.auth import token_auth
from app.models import User as Usr


class Users(Resource):

    def post(self):
        """API endpoint for creating a user

        :return: status code 405 - invalid JSON or invalid request type
        :return: status code 400 - unsupported Content-Type
        :return: status code 409 - username conflict
        :return: status code 201 - successful submission
        """

        # Ensure post's Content-Type is supported
        if request.is_json:
            # Ensure data is a valid JSON
            json_request = request.get_json(silent=True)

            if json_request:
                user, errors = Usr.load(json_request)

                if errors:
                    current_app.logger.info(
                        'Error deserializing json to User [{}]'.format(json_request))
                    return make_response(jsonify(errors), 405)

                if Usr.query.filter_by(username=user.username).first() is not None:
                    current_app.logger.info(
                        'Username already taken [{}]'.format(user.username))
                    return make_response(jsonify(errors), 409)

                user.save()
                current_app.logger.info(
                    'Created new user [{}]'.format(user.id))
                return user.dump().data, 201

            current_app.logger.info('Invalid JSON')
            return make_response(jsonify(error="Invalid Json!"), 405)

        current_app.logger.info('Unsupported Content-Type')
        return make_response(jsonify(error="Unsupported Content-Type!"), 400)


class User(Resource):

    decorators = [token_auth.login_required]

    def patch(self, id):
        """API endpoint for updating a user

        :param id: id of user to update

        :return: status code 404 - user not found
        :return: status code 200 - successful update
        :return: status code 400 - unsupported Content-Type
        :return: status code 403 - forbidden
        """
        # TODO validate data!

        # content type needs to be application/json.
        data = request.get_json(silent=True)
        if data:
            user = Usr.query.get(id)
            if user:
                if user != g.current_user:
                    return make_response(jsonify(error="Forbidden!"), 403)

                user.update(**data)
                current_app.logger.info('Updated user [{}]'.format(id))
                return user.dump().data, 200

            current_app.logger.info('Unable to find user [{}]'.format(id))
            return make_response(jsonify(error="User not found!"), 404)

        current_app.logger.info('Content-type not accepted')
        return make_response(jsonify(error="Unsupported Content-Type!"), 400)
