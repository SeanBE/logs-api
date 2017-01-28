import json
import pytest
import datetime
from flask import jsonify, url_for
from pytest_factoryboy import register

import app.models as m
from tests.factories import ExerciseFactory

register(ExerciseFactory, 'exercise1')
register(ExerciseFactory, 'exercise2')
register(ExerciseFactory, 'exercise3')


def test_put_workouts(client):
    response = client.put(url_for('api.workouts'))
    assert response.status_code == 405
    assert response.content_type == 'application/json'
    assert b'The method is not allowed for the requested URL.' in response.data


@pytest.mark.parametrize("exercise1__name", ["Exercise 1"])
@pytest.mark.parametrize("exercise2__name", ["Exercise 2"])
@pytest.mark.parametrize("exercise3__name", ["Exercise 3"])
def test_post_workout(client, user, exercise1, exercise2, exercise3):

    new_workout = {
        'date_proposed': '2016-11-11',
        'entries': [
            {'exercise': {'name': exercise1.name}, 'sets': [
                {'reps': 8, 'weight': 0, 'comment': None},
                {'reps': 10, 'weight': 0, 'comment': None},
                {'reps': 12, 'weight': 0, 'comment': None}]},
            {'exercise': {'name': exercise2.name}, 'sets': [
                {'reps': 6, 'weight': 0, 'comment': None},
                {'reps': 7, 'weight': 0, 'comment': None},
                {'reps': 8, 'weight': 0, 'comment': None}]},
            {'exercise': {'name': exercise3.name}, 'sets': [
                {'reps': 3, 'weight': 0, 'comment': None},
                {'reps': 4, 'weight': 0, 'comment': None},
                {'reps': 5, 'weight': 0, 'comment': None}]}]}

    exercises = m.Exercise.query.all()
    response = client.post(url_for('api.workouts'), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    }, data=json.dumps(new_workout), content_type='application/json')

    assert response.status_code == 201
    json_response = json.loads(response.get_data(as_text=True))
    assert json_response['id'] == 1
    assert json_response['comment'] is None
    assert json_response['date_completed'] is None
    assert json_response['date_proposed'] == new_workout['date_proposed']

    first_entry = json_response['entries'][0]
    assert first_entry['exercise'].keys() == {'name', 'id'}
    assert first_entry['sets'][0].keys() == {'weight', 'comment', 'id', 'reps', 'bodyweight'}
    assert user.workouts.count() == 1


def test_get_workout(client, user, workout):
    response = client.get(url_for('api.workout', id=workout.id), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    })

    assert response.status_code == 200
    json_response = json.loads(response.get_data(as_text=True))
    workout_dump = workout.dump().data
    assert workout_dump['date_proposed'] == json_response['date_proposed']
    assert workout_dump['entries'] == json_response['entries']
    assert user.workouts.count() == 1


@pytest.mark.parametrize('workouts', [(3)], indirect=True)
def test_get_all_workouts(client, user, workouts):

    response = client.get(url_for('api.workouts'), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    })

    assert response.status_code == 200
    json_response = json.loads(response.get_data(as_text=True))
    assert len(json_response) == len(workouts)
    assert user.workouts.count() == len(workouts)


def test_delete_workout(client, user, workout):

    response = client.delete(url_for('api.workout', id=workout.id), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    })

    assert response.status_code == 204
    assert response.content_type == 'application/json'
    assert str(response.data) == "b''"
    assert m.Workout.query.get(workout.id) is None
    assert user.workouts.count() == 0


def test_patch_workout(client, db, user, workout):
    data = workout.dump().data

    data['date_completed'] = None
    data['date_proposed'] = None

    for exercise in data['entries']:
        for exercise_set in exercise['sets']:
            exercise_set['weight'] = 100
            exercise_set['comment'] = 'Good'

    response = client.patch(url_for('api.workout', id=workout.id), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    }, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 200
    json_response = json.loads(response.get_data(as_text=True))
    assert json_response['id'] == workout.id
    assert all(([all([s['weight'] == 100 for s in e['sets']])
                 for e in data['entries']]))
    assert user.workouts.first().id == workout.id


@pytest.mark.parametrize("exercise1__name", ["Exercise 1"])
def test_patch_workout_different_exercise(client, db, user, workout, exercise1):
    data = workout.dump().data

    data['date_completed'] = None
    data['date_proposed'] = None

    assert data['entries'][0]['exercise'] != exercise1.name
    data['entries'][0]['exercise'] = exercise1.dump().data

    response = client.patch(url_for('api.workout', id=workout.id), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    }, data=json.dumps(data), content_type='application/json')

    assert response.status_code == 200
    json_response = json.loads(response.get_data(as_text=True))
    assert json_response['id'] == workout.id
    assert user.workouts.first().id == workout.id
    assert json_response['entries'][0]['exercise']['name'] == exercise1.name


def test_workout_not_found(client, user):

    response = client.get(url_for('api.workout', id=1), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    })

    json_response = json.loads(response.get_data(as_text=True))
    print(json_response)
    assert response.status_code == 404
    assert json_response.keys() == {'status', 'message'}
    assert json_response['status'] == 404
    assert json_response['message'] == 'Workout with ID [1] does not exist.'
