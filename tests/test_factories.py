from pytest_factoryboy import register
import tests.factories as f


# def test_factory():
#
#     sets1 = f.SetEntryFactory.create_batch(4)
#     entry1 = f.ExerciseEntryFactory(sets=sets1)
#
#     sets2 = f.SetEntryFactory.create_batch(4)
#     entry2 = f.ExerciseEntryFactory(sets=sets2)
#     workout = f.WorkoutFactory(exercises=[entry1, entry2])
#
#     print(workout.exercises[0].ex_num)
#     print(workout.exercises[1].ex_num)
#     print(workout.dump().data)
