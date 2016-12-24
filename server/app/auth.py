from flask import jsonify, make_response

from app.models import User
from app.extensions import auth


@auth.error_handler
def unauthorized():
    # or 403..
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@auth.verify_password
def verify_password(username, password):
    if not username or not password:
        return False

    user = User.query.filter_by(username=username).first()
    if user is None or not user.verify_password(password):
        return False

    return True
