from marshmallow import Schema, fields, post_load

from .base import Base
from app.extensions import db
from app.models.set_entry import SetEntrySchema


class ExerciseEntry(Base):
    __table__name = 'exercise_entry'
    __table_args__ = (db.UniqueConstraint('exercise_id', 'workout_id',
                                          name='_exercise_workout_uc'),)

    workout_id = db.Column(db.Integer,
                           db.ForeignKey('workout.id'), nullable=False)

    ex_num = db.Column(db.Integer, nullable=False)
    exercise = db.relationship('Exercise')
    exercise_id = db.Column(db.Integer,
                            db.ForeignKey('exercise.id'), nullable=False)

    sets = db.relationship('SetEntry', backref="exercise_entry",
                           cascade="all, delete-orphan",
                           order_by=('(SetEntry.set_num)'))


class ExerciseEntrySchema(Schema):

    name = fields.String(attribute='exercise.name')
    sets = fields.Nested(SetEntrySchema, many=True, required=True)

    @post_load
    def make_entry(self, data):
        return ExerciseEntry(**data)
