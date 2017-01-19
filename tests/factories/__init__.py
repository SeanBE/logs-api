import datetime
import factory
import factory.fuzzy
from faker import Factory as FakeFactory

from app.extensions import db
from app.models import Exercise, ExerciseEntry, SetEntry, Workout

faker = FakeFactory.create()


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):

    id = factory.Sequence(lambda n: n)

    class Meta:
        abstract = True
        sqlalchemy_session = db.session


class ExerciseFactory(BaseFactory):

    name = factory.Sequence(lambda n: 'Exercise #{}'.format(n))

    class Meta:
        model = Exercise


class WorkoutFactory(BaseFactory):

    date_proposed = datetime.date.today()
    date_completed = datetime.date.today()
    comment = factory.fuzzy.FuzzyText()

    @factory.post_generation
    def exercises(self, create, extracted, **kwargs):
        if extracted:
            for exercise in extracted:
                self.exercises.append(exercise)

    class Meta:
        model = Workout


class ExerciseEntryFactory(BaseFactory):

    # Assume workout_id auto assigned.
    workout_id = factory.SubFactory(WorkoutFactory)
    ex_num = factory.Sequence(lambda n: n)

    # Assume exercise_id auto set.
    exercise = factory.SubFactory(ExerciseFactory)

    @factory.post_generation
    def sets(self, create, extracted, **kwargs):
        if extracted:
            for exercise in extracted:
                self.sets.append(exercise)

    class Meta:
        model = ExerciseEntry


class SetEntryFactory(BaseFactory):

    set_num = factory.Sequence(lambda n: n)
    reps = factory.fuzzy.FuzzyInteger(20)
    weight = factory.fuzzy.FuzzyInteger(1000)
    comment = factory.fuzzy.FuzzyText()
    entry_id = factory.SubFactory(ExerciseEntryFactory)

    class Meta:
        model = SetEntry
