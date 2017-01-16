import json
from datetime import date, datetime
import app.models as m
from app.extensions import db

# TODO update with factory-boy.


def test_workout_update():
    workout = m.Workout(date_proposed=date.today())

    exercise1 = m.Exercise(name='ABC')
    exercise2 = m.Exercise(name='DEF')
    exercise3 = m.Exercise(name='GHI')

    exercises = [exercise1, exercise2, exercise3]
    for index, ex in enumerate(exercises):
        s1 = m.SetEntry(reps=10, set_num=0, weight=0)
        s2 = m.SetEntry(reps=10, set_num=1, weight=0)
        s3 = m.SetEntry(reps=10, set_num=2, weight=0)
        entry = m.ExerciseEntry(ex_num=index, exercise=ex, sets=[s1, s2, s3])
        workout.exercises.append(entry)

    db.session.add(workout)
    db.session.commit()

    saved_workout = m.Workout.query.first()
    assert saved_workout is not None

    data, errors = saved_workout.dump()

    data['comment'] = 'Great stuff!'

    # These don't get updated.
    data['date_proposed'] = None
    data['date_completed'] = None

    data['exercises'][0]['sets'][1]['weight'] = 100

    saved_workout.update(**data)
    updated, errors = saved_workout.dump()

    assert updated['date_completed'] is None
    assert updated['date_proposed'] is not None
    assert updated['comment'] == data['comment']
    assert updated['exercises'][0]['sets'][1]['weight'] == 100


def test_db_relationships():
    workout = m.Workout(date_proposed=date.today())

    exercise1 = m.Exercise(name='ABC')
    exercise2 = m.Exercise(name='DEF')
    exercise3 = m.Exercise(name='GHI')

    exercises = [exercise1, exercise2, exercise3]
    for index, ex in enumerate(exercises):
        s1 = m.SetEntry(reps=10, set_num=0, weight=0)
        s2 = m.SetEntry(reps=10, set_num=1, weight=0)
        s3 = m.SetEntry(reps=10, set_num=2, weight=0)
        entry = m.ExerciseEntry(ex_num=index, exercise=ex, sets=[s1, s2, s3])
        workout.exercises.append(entry)

    db.session.add(workout)
    db.session.commit()

    workout = m.Workout.query.first()
    assert workout is not None
    assert workout.date_proposed == date.today()
    assert workout.date_completed is None
    assert workout.comment is None

    for entry_index, entry in enumerate(workout.exercises):
        assert entry.exercise in exercises
        assert entry.ex_num == entry_index
        assert entry.exercise_id in [e.id for e in exercises]
        assert len(entry.sets) == 3
        for index, s in enumerate(entry.sets):
            assert s.set_num == index
            assert s.reps == 10
            assert s.weight == 0


def test_json():
    workout = m.Workout(date_proposed=date.today())

    exercise1 = m.Exercise(name='ABC')
    exercise2 = m.Exercise(name='DEF')
    exercise3 = m.Exercise(name='GHI')

    exercises = [exercise1, exercise2,exercise3]
    for index, ex in enumerate(exercises):
        s1 = m.SetEntry(reps=10, set_num=0, weight=0)
        s2 = m.SetEntry(reps=10, set_num=1, weight=0)
        s3 = m.SetEntry(reps=10, set_num=2, weight=0)
        entry = m.ExerciseEntry(ex_num=index, exercise=ex, sets=[s1, s2, s3])
        workout.exercises.append(entry)

    db.session.add(workout)
    db.session.commit()

    data, errors = workout.dump()
    assert data['date_proposed'] == date.today().isoformat()
    assert data['date_completed'] is None
    assert data['comment'] is None
    assert data['id'] == 1

    sorted(workout.exercises, key=lambda x: x.ex_num)

    combined_exercises = zip(data['exercises'], workout.exercises)
    for index, [json_entry, db_entry] in enumerate(combined_exercises):
        assert index == db_entry.ex_num
        assert json_entry['exercise']['name'] == db_entry.exercise.name

        assert len(json_entry['sets']) == 3
        combined_sets = zip(json_entry['sets'], db_entry.sets)
        for index, [json_set, db_set] in enumerate(combined_sets):
            assert index == db_set.set_num
            assert json_set['reps'] == db_set.reps
            assert json_set['weight'] == db_set.weight
