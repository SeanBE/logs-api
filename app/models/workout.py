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
    # TODO rename to entries.
    exercises = fields.Nested(ExerciseEntrySchema, many=True, required=True)

    @post_load
    def make_workout(self, data):
        for index, entry in enumerate(data['exercises']):
            entry.ex_num = index

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

    def update(self, commit=True, **kwargs):
        kwargs.pop('id', None)

        for entry, db_entry in zip(kwargs['exercises'], self.exercises):
            for key, value in entry['exercise'].items():
                if value is not None:
                    setattr(db_entry.exercise, key, value)

            for new_set, db_set in zip(entry['sets'], db_entry.sets):
                for key, value in new_set.items():
                    if value is not None:
                        setattr(db_set, key, value)
    
        kwargs.pop('exercises', None)
        return super(Base, self).update(**kwargs)
