from flask_httpauth import HTTPBasicAuth
# from flask import g, jsonify, session

auth = HTTPBasicAuth()
users = {'user': 'password'}


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

# @auth.error_handler
# def auth_error():
#     return "&lt;h1&gt;Access Denied&lt;/h1&gt;"
    
# @basic_auth.verify_password
# def verify_password(nickname, password):
#     """Password verification callback."""
#     if not nickname or not password:
#         return False
#     user = User.query.filter_by(nickname=nickname).first()
#     if user is None or not user.verify_password(password):
#         return False
#     if user.ping():
#         from .events import push_model
#         push_model(user)
#     db.session.add(user)
#     db.session.commit()
#     g.current_user = user
#     return True
