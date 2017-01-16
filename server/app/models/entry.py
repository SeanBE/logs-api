from collections import defaultdict
from marshmallow import Schema, fields, post_dump, post_load, pre_load
from itertools import groupby

from .base import Base
from app.extensions import db
from app.models.exercise import Exercise


class ExerciseEntry(Base):
    __table__name = 'exercise_entry'
    __table_args__ = (db.UniqueConstraint('set_num', 'exercise_id', 'workout_id',
                                          name='_exercise_set_workout_uc'),)

    set_num = db.Column(db.Integer, nullable=False)
    ex_num = db.Column(db.Integer, nullable=False)
    exercise = db.relationship('Exercise')
    exercise_id = db.Column(db.Integer, db.ForeignKey(
        'exercise.id'), nullable=False)

    workout_id = db.Column(db.Integer, db.ForeignKey(
        'workout.id'), nullable=False)

    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    def __init__(self, exercise_name=None, **kwargs):
        self.exercise = Exercise.query.filter_by(name=exercise_name).first()
        if self.exercise:
            self.exercise_id = self.exercise.id

        super(ExerciseEntry, self).__init__(**kwargs)


class ExerciseEntrySchema(Schema):

    exercise = fields.String(attribute='exercise.name')
    reps = fields.Integer(required=True)
    weight = fields.Integer(allow_none=True)
    comment = fields.String(allow_none=True)

    # TODO can we get rid of these two fields on the schema level?
    set_num = fields.Integer(required=True)
    ex_num = fields.Integer(required=True)

    @post_dump(pass_many=True)
    def fix_entries(self, data, many):
        if many:
            exercises = []
            # TODO This efficient?
            data = sorted(data, key=lambda k: k['ex_num'])
            for exercise, rest in groupby(data, lambda e: e["exercise"]):
                rest = sorted(rest, key=lambda k: k['set_num'])
                sets = [{k: v for k, v in d.items() if k not in [
                    'exercise', 'set_num', 'ex_num']} for d in rest]
                exercises.append({"name": exercise, "sets": sets})
            return exercises
        return data

    @post_load
    def make_entry(self, data):
        data['exercise_name'] = data.pop('exercise.name')
        return ExerciseEntry(**data)
