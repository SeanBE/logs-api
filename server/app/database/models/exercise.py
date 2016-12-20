from app.database import db
from marshmallow import Schema, fields, post_load
from app.database.mixins import MarshmallowMixin, CRUDMixin


class ExerciseSchema(Schema):

    id = fields.Integer(required=True, dump_only=True)
    name = fields.String(required=True)

    @post_load
    def make_exercise(self, data):
        return Exercise(**data)


class Exercise(CRUDMixin, MarshmallowMixin, db.Model):

    __tablename__ = 'exercise'
    __schema__ = ExerciseSchema

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
