import json
import unittest
from random import randint
from datetime import datetime

from app import create_app
from app.extensions import db
from app.models import Exercise, Workout, ExerciseEntry

EXERCISES = ['Bench Press', 'Squat', 'Deadlift']
DATES = ['2016-11-01', '2016-11-02', '2016-11-03']

# TODO testcase very similar to exercisetestcase..


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
        assert EXERCISES[0] in data['exercises'].keys()

        first_exercise = data['exercises'].get(EXERCISES[0])
        assert len(first_exercise) == 3
        for idx, ex_set in enumerate(first_exercise):
            assert idx == ex_set['set_num']

    def test_delete_workout(self):
        workout = Workout.query.filter_by(id=1).first()
        assert workout is not None
        deleted = workout.delete()

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

        data = {
            "date_proposed": "2016-10-05",
            "exercises": {
                "Bench Press": [{
                    "comment": "Awesome!!",
                    "reps": 5,
                    "set_num": 0,
                    "weight": 62
                }],
                "Deadlift": [{
                    "comment": "Comment",
                    "reps": 2,
                    "set_num": 0,
                    "weight": 197
                }]
            }
        }

        workout = Workout.load(data).save()
        data, errors = workout.dump()

        assert errors == {}
        assert data['id'] > 3
        assert data['date_proposed'] == "2016-10-05"
        # TODO can this be cleaner?
        assert data['exercises']['Bench Press'][0]['reps'] == 5

    def test_update_workout(self):
        date_completed = '2016-11-05'

        workout = Workout.query.filter_by(id=1).first()
        data = workout.dump().data

        data['date_completed'] = create_date(date_completed)
        data['date_proposed'] = create_date(data['date_proposed'])
        data['exercises']['Bench Press'][0]['reps'] = 9999

        data.pop('id')
        data.pop('date_created')

        exercises = []
        for key, values in data['exercises'].items():
            for entry in values:
                entry['exercise'] = key
                exercises.append(entry)
        data['exercises'] = exercises

        for new_ex, exercise in zip(data['exercises'], workout.exercises):
            new_ex['exercise_name'] = new_ex.pop('exercise')
            for key, value in new_ex.items():
                setattr(exercise, key, value)

        data.pop('exercises')
        workout.update(**data)
        new_workout, errors = workout.dump()

        assert errors == {}
        assert new_workout['id'] == workout.id
        assert new_workout['date_completed'] == date_completed
        assert new_workout['exercises']['Bench Press'][0]['reps'] == 9999


def create_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d")

if __name__ == '__main__':
    unittest.main()
