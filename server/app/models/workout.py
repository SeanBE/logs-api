from datetime import datetime, date
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import Schema, fields, pre_load, post_load, ValidationError

from .base import Base
from app.extensions import db
from app.models.entry import ExerciseEntrySchema


class WorkoutSchema(Schema):

    id = fields.Integer(dump_only=True)

    date_proposed = fields.Date(required=True)
    date_completed = fields.Date(allow_none=True)
    comment = fields.String(allow_none=True)
    exercises = fields.Nested(ExerciseEntrySchema, many=True, required=True)

    @pre_load
    def fix_exercise_entries(self, data):

        exercises = []
        for key, values in data['exercises'].items():
            for idx, entry in enumerate(values):
                entry['exercise'] = key
                exercises.append(entry)

        data['exercises'] = exercises

        return data

    @post_load
    def make_workout(self, data):
        return Workout(**data)


class Workout(Base):
    __tablename__ = 'workout'
    __schema__ = WorkoutSchema

    date_completed = db.Column(db.Date)
    date_proposed = db.Column(db.Date, default=date.today(), nullable=False)
    comment = db.Column(db.Text)

    exercises = db.relationship('ExerciseEntry', backref="workout", cascade="all, delete-orphan",
                                lazy='dynamic', order_by=('ExerciseEntry.exercise_id'))
