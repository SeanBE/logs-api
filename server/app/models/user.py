import time
from flask import abort
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.mixins import CRUDMixin


def timestamp():
    """Return the current timestamp as an integer."""
    return int(time.time())


class User(db.Model, CRUDMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.Integer, default=timestamp)
    updated_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)

    username = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def create(data):
        """Create a new user."""
        user = User()
        user.from_dict(data, partial_update=False)
        return user

    def from_dict(self, data, partial_update=True):
        for field in ['username', 'password']:
            try:
                setattr(self, field, data[field])
            except KeyError:
                if not partial_update:
                    abort(400)
