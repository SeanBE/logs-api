import unittest
from random import randint
from datetime import datetime

from app import create_app, config
from app.database import db
from app.database.models import Exercise, ExerciseEntry, Workout
from app.database.services import DatabaseService


EXERCISES = ['Bench Press', 'Squat', 'Deadlift']


class ServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config.TestConfig)
        db.app = self.app
        self.app = self.app.test_client()

        db.session.remove()
        db.drop_all()
        db.create_all()

        self.add_exercises(EXERCISES)
        self.add_workouts()

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

    def add_workouts(self):

        for proposed_date in ['2016-11-01', '2016-11-02', '2016-11-03']:
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
        workouts = DatabaseService().get_list()
        assert len(workouts) == 3

    def test_exercises_exist(self):
        # TODO remove.
        squat = Exercise.query.filter_by(name='Squat').first()
        assert squat is not None

    def test_workouts_exist(self):
        # TODO remove.
        workout = Workout.query.filter_by(date_proposed='2016-11-01').first()
        assert workout is not None


def create_date(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d")

if __name__ == '__main__':
    unittest.main()
