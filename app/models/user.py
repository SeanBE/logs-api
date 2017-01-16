import os
import binascii
from marshmallow import Schema, fields, post_load
from werkzeug.security import generate_password_hash, check_password_hash

from .base import Base
from app.extensions import db


class UserSchema(Schema):

    id = fields.Integer(required=True, dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)

    @post_load
    def make_user(self, data):
        return User(**data)


class User(Base):
    __tablename__ = 'users'
    __schema__ = UserSchema

    username = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)

    token = db.Column(db.String(64), nullable=True, unique=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.token = None
        self.password_hash = generate_password_hash(password)

    def generate_token(self):
        """Creates a 64 character long randomly generated token."""
        self.token = binascii.hexlify(os.urandom(32)).decode('utf-8')
        return self.token

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
