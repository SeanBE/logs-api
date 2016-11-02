import os
import unittest

from flask import json
from app import create_app, config
from app.database import psql as db
from app.database.models import Exercise, ExerciseEntry, Workout

class ServiceTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a blank temp database before each test"""

        # TODO test config??
        app = create_app(config.DevConfig)
        db.app = app
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        # Insert exercises
        bench_press = Exercise(name='Bench Press')
        deadlift = Exercise(name='Deadlift')
        db.session.add(bench_press)
        db.session.add(deadlift)

        # Commit the changes for the users
        db.session.commit()

        # Insert workouts.
        # completed_workout = Workout('John', '2016-11-01')
        # e1 = ExerciseEntry(bench_press, 0, 10, 120)
        # e2 = ExerciseEntry(bench_press, 1, 10, 140)
        # e3 = ExerciseEntry(bench_press, 2, 10, 160)
        # e4 = ExerciseEntry(deadlift, 0, 1, 200)
        # e5 = ExerciseEntry(deadlift, 1, 3, 220)
        # e6 = ExerciseEntry(deadlift, 2, 5, 240)
        #
        # completed_workout.exercises = [e1,e2,e3,e4,e5,e6]
        # completed_workout.date_completed = '2016-11-02'
        #
        # db.session.add(completed_workout)
        #
        # new_workout = Workout('John', '2016-11-03')
        # e1 = ExerciseEntry(bench_press, 0, 10, 120)
        # e2 = ExerciseEntry(bench_press, 1, 10, 140)
        # e3 = ExerciseEntry(bench_press, 2, 10, 160)
        # e4 = ExerciseEntry(deadlift, 0, 1, 200)
        # e5 = ExerciseEntry(deadlift, 1, 3, 220)
        # e6 = ExerciseEntry(deadlift, 2, 5, 240)
        #
        # new_workout.exercises = [e1,e2,e3,e4,e5,e6]
        #
        # db.session.add(new_workout)
        #
        # db.session.commit()


    def tearDown(self):
        """Destroy blank temp database after each test"""
        # db.drop_all()



    # def test_service_get_all(self):
        # exercises = Exercise.query.first()
        # self.assertEqual(len(exercises), 2)


    def test_index(self):
        """inital test. ensure flask was set up correctly"""
        response = self.app.get('/api/1/', content_type='html/text')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
