from flask import g, jsonify, make_response, current_app
from flask_restful import Resource

from app.auth import user_auth, token_auth


class Token(Resource):

    @user_auth.login_required
    def post(self):
        """API endpoint for generating a token for current user

        :return: status code 200 - successful token generated and retrieved
        """
        if g.current_user.token is None:
            g.current_user.generate_token()
            g.current_user.save()

        current_app.logger.info(
            'Generating token for user {}.'.format(g.current_user.username))
        return make_response(jsonify({'token': g.current_user.token}), 200)

    @token_auth.login_required
    def delete(self):
        """API endpoint for deleting current user token

        :return: status code 204 - successful token removal
        """
        g.current_user.token = None
        g.current_user.save()

        current_app.logger.info(
            'Deleting token for user {}.'.format(g.current_user.username))
        return '', 204
