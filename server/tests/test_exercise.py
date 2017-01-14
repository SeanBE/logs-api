import unittest

from app import create_app
from app.extensions import db
from app.models import Exercise

EXERCISES = ['Bench Press', 'Squat', 'Deadlift']

# TODO revamp To test mixins purely.
class ExerciseTestCase(unittest.TestCase):
    """
    Tests with CrudMixin and MarshMallow Mixin with Exercise object.
    """

    def setUp(self):
        self.app = create_app('testing')
        db.app = self.app
        self.app = self.app.test_client()

        # session remove needed?
        db.session.remove()
        db.drop_all()
        db.create_all()

        self.add_exercises(EXERCISES)

    def add_exercises(self, exercises):
        for exercise_name in exercises:
            exercise = Exercise(name=exercise_name)
            db.session.add(exercise)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_exercise(self):
        exercise = Exercise.query.filter_by(id=1).first()

        assert exercise is not None
        data, errors = exercise.dump()

        assert errors == {}
        assert data['id'] == 1
        assert data['name'] in EXERCISES
        assert all(key in ['id', 'name'] for key in data)

    def test_delete_exercise(self):
        exercise = Exercise.query.filter_by(id=1).first()
        assert exercise is not None
        deleted = exercise.delete()

        exercise = Exercise.query.filter_by(id=1).first()
        assert exercise is None

    def test_get_list(self):
        exercises = (Exercise
                     .query
                     .all())

        data, errors = Exercise.dump_list(exercises)

        assert errors == {}
        assert len(data) == 3

    def test_create_exercise(self):
        name = 'Glute Bridge123'

        exercise, errors = Exercise.load({'name': name})
        exercise.save()
        data, errors = exercise.dump()

        assert errors == {}
        assert data['id'] > 3
        assert data['name'] == 'Glute Bridge123'

    def test_update_exercise(self):
        new_name = 'Squat 2'
        data = {
            'name': new_name
        }
        exercise = Exercise.query.filter_by(name='Squat').first()

        exercise.update(**data)
        data, errors = exercise.dump()

        assert errors == {}
        assert data['id'] == exercise.id
        assert data['name'] == new_name


if __name__ == '__main__':
    unittest.main()
