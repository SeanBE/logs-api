import json
import unittest
import datetime
from random import randint

from app import create_app
from app.extensions import db
from app.models import Exercise, Workout, ExerciseEntry
from app.models.workout import WorkoutSchema

EXERCISES = ['Bench Press', 'Squat', 'Deadlift']
DATES = ['2016-11-01', '2016-11-02', '2016-11-03']


# TODO testcase very similar to Exercise Test case...
class WorkoutTestCase(unittest.TestCase):
    """
    Tests with CrudMixin and MarshMallow Mixin with Workout object.
    """

    def setUp(self):
        self.app = create_app('testing')
        db.app = self.app
        self.app = self.app.test_client()

        db.session.remove()
        db.drop_all()
        db.create_all()

        self.add_exercises(EXERCISES)
        self.add_workouts(DATES)

    def add_exercises(self, exercises):
        for exercise_name in exercises:
            exercise = Exercise(name=exercise_name)
            db.session.add(exercise)

        db.session.commit()

    def create_sets(self, ex_name):

        entries = []

        for set_num in range(3):
            reps = randint(0, 12)
            weight = randint(0, 200)

            entry = ExerciseEntry(ex_name, set_num, reps, weight, 'Comment')
            entries.append(entry)

        return entries

    def add_workouts(self, dates):

        for proposed_date in dates:
            workout = Workout(date_proposed=create_date(proposed_date))

            for exercise_name in EXERCISES:
                exercise_sets = self.create_sets(exercise_name)
                workout.exercises.extend(exercise_sets)

            db.session.add(workout)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_workout(self):

        workout = Workout.query.filter_by(id=1).first()
        assert workout is not None

        data, errors = workout.dump()
        assert errors == {}
        assert EXERCISES[0] in [ex['name'] for ex in data['exercises']]

        first_exercise = data['exercises'][0]
        assert len(first_exercise['sets']) == 3

    def test_delete_workout(self):
        workout = Workout.query.filter_by(id=1).first()
        assert workout is not None

        # TODO this output is None??
        workout.delete()

        workout = Workout.query.filter_by(id=1).first()
        assert workout is None

    def test_get_workouts(self):
        workouts = (Workout
                    .query
                    .all())

        data, errors = Workout.dump_list(workouts)

        assert errors == {}
        assert len(data) == 3

    def test_create_workout(self):

        data = {'comment': None,
                'exercises': [
                    {'name': 'Bench Press',
                     'sets': [{'comment': 'Comment', 'weight': 20, 'reps': 10},
                              {'comment': 'Comment', 'weight': 160, 'reps': 7},
                              {'comment': 'Comment', 'weight': 129, 'reps': 11}]},
                    {'name': 'Squat',
                     'sets': [{'comment': 'Comment', 'weight': 94, 'reps': 1},
                              {'comment': 'Comment', 'weight': 36, 'reps': 1},
                              {'comment': 'Comment', 'weight': 167, 'reps': 6}]},
                    {'name': 'Deadlift',
                     'sets': [{'comment': 'Comment', 'weight': 133, 'reps': 0},
                              {'comment': 'Comment', 'weight': 45, 'reps': 4},
                              {'comment': 'Comment', 'weight': 53, 'reps': 10}]}],
                'date_completed': None,
                'date_proposed': '2016-10-05'}

        workout, errors = Workout.load(data)
        workout.save()
        data, errors = workout.dump()

        assert errors == {}
        assert data['id'] > 3
        assert data['date_proposed'] == "2016-10-05"
        assert data['exercises'][0]["sets"][0]["reps"] == 10

    def test_update_workout(self):
        date_completed = '2016-11-05'
        workout = Workout.query.filter_by(id=1).first()
        data, errors = workout.dump()

        data['date_completed'] = datetime.date(2016, 11, 5)
        data['date_proposed'] = create_date(data['date_proposed'])
        data['exercises'][0]["sets"][0]['reps'] = 9999

        data.pop('id', None)
        data = WorkoutSchema().fix_exercise_entries(data)
        for new_ex, exercise in zip(data['exercises'], workout.exercises):
            new_ex['exercise_name'] = new_ex.pop('exercise')
            for key, value in new_ex.items():
                setattr(exercise, key, value)
        data.pop('exercises', None)

        workout.update(**data)
        new_workout, errors = workout.dump()

        updated = Workout.query.filter_by(id=1).first()
        assert updated.id == workout.id
        assert updated.date_completed == data['date_completed']
        assert new_workout['exercises'][0]['sets'][0]['reps'] == 9999


def create_date(date_string):
    return datetime.datetime.strptime(date_string, "%Y-%m-%d")

if __name__ == '__main__':
    unittest.main()
