import json
import unittest
from random import randint
from datetime import datetime

from app import create_app, config
from app.database import db
from app.database.models import Exercise, ExerciseEntry, Workout
from app.database.services import DatabaseService


EXERCISES = ['Bench Press', 'Squat', 'Deadlift']
DATES = ['2016-11-01', '2016-11-02', '2016-11-03']

class ServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config.TestConfig)
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
            workout = Workout(create_date(proposed_date))

            for exercise_name in EXERCISES:
                exercise_sets = self.create_sets(exercise_name)
                workout.exercises.extend(exercise_sets)

            db.session.add(workout)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_all_exercises(self):
        workouts, errors = DatabaseService().get_list(10, 0)

        assert errors is None
        assert len(workouts) == 3

        workout = next((w for w in workouts if w[
                       'date_proposed'] == DATES[0]), None)

        assert workout is not None
        assert EXERCISES[0] in workout['exercises'].keys()
        assert len(workout['exercises'].get(EXERCISES[0])) == 3

    def test_get_all_with_limit(self):
        workouts, _ = DatabaseService().get_list(2, 0)

        assert len(workouts) == 2

        workout = next((w for w in workouts if w[
                       'date_proposed'] == DATES[-1]), None)

        assert workout is None

    def test_get_all_with_offset(self):
        workouts, _ = DatabaseService().get_list(10, 1)

        assert len(workouts) == 2

        workout = next((w for w in workouts if w[
                       'date_proposed'] == DATES[0]), None)

        assert workout is None

    def test_get_exercise(self):
        w = Workout.query.filter_by(date_proposed='2016-11-01').first()
        assert w is not None

        workout, errors = DatabaseService().get(w.id)
        assert workout is not None
        assert errors is None

        assert EXERCISES[0] in workout['exercises'].keys()
        first_exercise = workout['exercises'].get(EXERCISES[0])
        assert len(first_exercise) == 3
        for idx, ex_set in enumerate(first_exercise):
            assert idx == ex_set['set_num']

    def test_create_exercise(self):
        with open('tests/data.json') as json_data:
            data = json.load(json_data)
            success, errors = DatabaseService().create(data)

        assert success
        assert errors is None
        saved_workout = Workout.query.filter_by(date_proposed=data['date_proposed']).first()
        assert saved_workout is not None

    def test_delete(self):
        date = '2016-11-20'
        self.add_workouts([date])
        w = Workout.query.filter_by(date_proposed=date).first()
        assert w is not None

        errors = DatabaseService().delete(w.id)
        self.assertFalse(errors)

    def test_update(self):
        # TODO make sure data coming in/out is orderd by exercise name and set_num
        with open('tests/data.json') as json_data:
            data = json.load(json_data)
            success, errors = DatabaseService().create(data)

        saved_workout = Workout.query.filter_by(date_proposed=data['date_proposed']).first()

        with open('tests/data.json') as json_data:
            data = json.load(json_data)

        data['date_completed'] = create_date('2016-10-06')
        data['date_proposed'] = create_date(data['date_proposed'])

        comment = 'Changed comment!'
        data['exercises']['Bench Press'][1]['comment'] = comment

        updated_workout, errors = DatabaseService().update(saved_workout.id, data)
        self.assertFalse(errors)
        assert updated_workout['exercises']['Bench Press'][1]['comment'] == comment


def create_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d")

if __name__ == '__main__':
    unittest.main()
