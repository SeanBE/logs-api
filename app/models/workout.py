from datetime import date
from marshmallow import Schema, fields, post_load

from .base import Base
from app.extensions import db
from app.models.exercise_entry import ExerciseEntrySchema


class WorkoutSchema(Schema):

    id = fields.Integer(dump_only=True)

    date_proposed = fields.Date(required=True)
    date_completed = fields.Date(allow_none=True)
    comment = fields.String(allow_none=True)
    exercises = fields.Nested(ExerciseEntrySchema, many=True, required=True)

    @post_load
    def make_workout(self, data):
        return Workout(**data)


class Workout(Base):
    __tablename__ = 'workout'
    __schema__ = WorkoutSchema

    comment = db.Column(db.Text)
    date_completed = db.Column(db.Date)
    date_proposed = db.Column(db.Date, default=date.today(), nullable=False)

    exercises = db.relationship('ExerciseEntry',
                                backref="workout",
                                cascade="all, delete-orphan",
                                order_by=('(ExerciseEntry.ex_num)'))

    # TODO test this!
    def update(self, commit=True, **kwargs):
        kwargs.pop('id', None)
        data = WorkoutSchema().fix_exercise_entries(kwargs)
        for new_ex, exercise in zip(data['exercises'], self.exercises):
            new_ex['exercise_name'] = new_ex.pop('exercise')
            for key, value in new_ex.items():
                setattr(exercise, key, value)

        data.pop('exercises', None)
        return super(Base, self).update(**data)
