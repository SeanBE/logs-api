from flask import g, request, jsonify, abort
from flask_restful import Resource

from app.auth import token_auth
from app.models import User as Usr


class Users(Resource):

    def post(self):

        data = request.get_json(force=True)
        user = Usr.load(data)

        if Usr.query.filter_by(username=user.username).first() is not None:
            abort(400)

        # user.save()
        return jsonify(user.dump().data), 201


class User(Resource):

    decorators = [token_auth.login_required]

    def put(self, id):
        user = Usr.query.get(id)

        if user != g.current_user:
            abort(403)

        # TODO force?
        data = request.get_json()
        user.update(**data)
        return '', 204
