from collections import defaultdict
from marshmallow import Schema, fields, post_dump, post_load

from app.extensions import db
from app.models.exercise import Exercise
from app.mixins import MarshmallowMixin, CRUDMixin


class ExerciseEntry(CRUDMixin, MarshmallowMixin, db.Model):
    __table__name = 'exercise_entry'
    __table_args__ = (db.UniqueConstraint('set_num', 'exercise_id', 'workout_id',
                                          name='_exercise_set_workout_uc'),)

    id = db.Column(db.Integer, primary_key=True)

    set_num = db.Column(db.Integer, nullable=False)

    exercise = db.relationship('Exercise')
    exercise_id = db.Column(db.Integer, db.ForeignKey(
        'exercise.id'), nullable=False)

    workout_id = db.Column(db.Integer, db.ForeignKey(
        'workout.id'), nullable=False)

    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    def __init__(self, exercise_name=None, set_num=None, reps=None, weight=None, comment=None):

        self.exercise = Exercise.query.filter_by(name=exercise_name).first()

        if self.exercise:
            self.exercise_id = self.exercise.id

        self.set_num = set_num
        self.reps = reps
        self.weight = weight
        self.comment = comment


class ExerciseEntrySchema(Schema):

    exercise = fields.String(attribute='exercise.name')
    reps = fields.Integer(required=True)
    set_num = fields.Integer(required=True)
    weight = fields.Integer(allow_none=True)
    comment = fields.String(allow_none=True)

    @post_dump(pass_many=True)
    def fix_entries(self, data, many):
        if many:
            exercises = defaultdict(list)
            for entry in data:
                exercises[entry['exercise']].append(
                    {k: v for k, v in entry.items() if k != 'exercise'})
            return exercises
        return data

    @post_load
    def make_entry(self, data):
        data['exercise_name'] = data.pop('exercise.name')
        return ExerciseEntry(**data)