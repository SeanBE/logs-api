import factory
import factory.fuzzy
from faker import Factory as FakeFactory

import app.models as models
from app.extensions import db

faker = FakeFactory.create()


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):

    id = factory.Sequence(lambda n: n)

    class Meta:
        abstract = True
        sqlalchemy_session = db.session


class ExerciseFactory(BaseFactory):

    name = factory.Sequence(lambda n: 'Exercise #{}'.format(n))

    class Meta:
        model = models.Exercise


# class EntryFactory(BaseFactory):
#
#     comment = factory.fuzzy.FuzzyText()
#     reps = factory.fuzzy.FuzzyInteger(20)
#     exercise_id = factory.SubFactory(ExerciseFactory)
#     set_num = factory.Sequence(lambda n: n)
#
#     set_num = db.Column(db.Integer, nullable=False)
#     ex_num = db.Column(db.Integer, nullable=False)
#
#
#     exercise_id = db.Column(db.Integer, db.ForeignKey(
#         'exercise.id'), nullable=False)
#
#     workout_id = db.Column(db.Integer, db.ForeignKey(
#         'workout.id'), nullable=False)
#
#     class Meta:
#         model = models.ExerciseEntry
#
#
# class WorkoutFactory(BaseFactory):
#
#     date_proposed = datetime.date.today()
#     comment = factory.fuzzy.FuzzyText()
#
#     @factory.post_generation
#     def exercises(self, create, extracted, **kwargs):
#         # for each exercise create 4 entries.
#         return EntryFactory.create_batch(4)
#
#     class Meta:
#         model = models.Workout
