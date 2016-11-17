from models import Workout, ExerciseEntry
from collections import defaultdict
from marshmallow import Schema, fields,pre_dump, post_dump, pre_load, post_load


class ExerciseEntrySchema(Schema):
    exercise = fields.String(attribute='exercise.name')
    reps = fields.Integer(required=True)
    set_num = fields.Integer(required=True)
    weight = fields.Integer(required=True)
    comment = fields.String(allow_none=True)

    @post_dump(pass_many=True)
    def wrap_if_many(self, data, many):
        if many:
            exercises = defaultdict(list)
            for entry in data:
                exercises[entry['exercise']].append(
                    {k: v for k, v in entry.items() if k != 'exercise'})
            return exercises
        return data

    @pre_dump(pass_many=True)
    def order_sets(self, data, many):
        # TODO order by setnum?
        pass

    @post_load
    def make_object(self, data):
        data['exercise_name'] = data.pop('exercise.name')
        return ExerciseEntry(**data)


class WorkoutSchema(Schema):
    # TODO URI/id
    date_created = fields.DateTime(dump_only=True)
    date_proposed = fields.Date(required=True)
    date_completed = fields.Date(allow_none=True)
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
    def make_object(self, data):
        return Workout(**data)
