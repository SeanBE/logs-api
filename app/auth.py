from flask import g, jsonify, make_response, current_app

from app.models import User
from app.extensions import user_auth, token_auth


@user_auth.error_handler
def unauthorized():
    current_app.logger.info('Unauthorized request via Basic Auth.')
    return (jsonify(message='Authentication Required', code=401), 401,
            {'WWW-Authenticate': 'Bearer realm="Authentication Required"'})


@user_auth.verify_password
def verify_password(username, password):
    if not username or not password:
        return False

    user = User.query.filter_by(username=username).first()
    if user is None or not user.verify_password(password):
        return False

    user.save()
    g.current_user = user
    current_app.logger.info('User {} verified by password.'.format(user.username))
    return True


@token_auth.verify_token
def verify_token(token, add_to_session=False):
    if add_to_session:
        if 'username' in session:
            del session['username']

    user = User.query.filter_by(token=token).first()
    if user is None:
        return False

    user.save()
    g.current_user = user
    current_app.logger.info('User {} verified by token.'.format(user.username))
    if add_to_session:
        session['username'] = user.username
    return True


@token_auth.error_handler
def token_error():
    current_app.logger.info('Unauthorized request via Token Auth.')
    return (jsonify(message='Authentication Required', code=401), 401,
            {'WWW-Authenticate': 'Bearer realm="Authentication Required"'})
