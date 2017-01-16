from marshmallow import Schema, fields, post_load

from .base import Base
from app.extensions import db


class ExerciseSchema(Schema):

    id = fields.Integer(required=True, dump_only=True)
    name = fields.String(required=True)

    @post_load
    def make_exercise(self, data):
        return Exercise(**data)


class Exercise(Base):

    __tablename__ = 'exercise'
    __schema__ = ExerciseSchema

    name = db.Column(db.String(120), unique=True, nullable=False)
