from flask import g, jsonify, make_response
from flask_restful import Resource

from app.auth import user_auth, token_auth


class Token(Resource):

    @user_auth.login_required
    def post(self):
        if g.current_user.token is None:
            g.current_user.generate_token()
            g.current_user.save()
        return make_response(jsonify({'token': g.current_user.token}), 200)

    @token_auth.login_required
    def delete(self):

        g.current_user.token = None
        g.current_user.save()

        return '', 204
