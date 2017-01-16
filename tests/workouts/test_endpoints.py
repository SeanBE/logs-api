import json
import pytest
import datetime
from flask import jsonify, url_for
import app.models as m


def test_put_workouts(client):
    response = client.put(url_for('api.workouts'))
    assert response.status_code == 405
    assert response.content_type == 'application/json'
    assert b'The method is not allowed for the requested URL.' in response.data


def test_post_workout(client, user):

    for ex in ['Exercise 1', 'Exercise 2', 'Exercise 3']:
        exercise, errors = m.Exercise.load({'name': ex})
        exercise.save()

    new_workout = {
        'date_proposed': '2016-11-11',
        'exercises': [
            {'name': 'Exercise 1', 'sets': [
                {'reps': 8, 'weight': 0, 'comment': None},
                {'reps': 10, 'weight': 0, 'comment': None},
                {'reps': 12, 'weight': 0, 'comment': None}]},
            {'name': 'Exercise 2', 'sets': [
                {'reps': 6, 'weight': 0, 'comment': None},
                {'reps': 7, 'weight': 0, 'comment': None},
                {'reps': 8, 'weight': 0, 'comment': None}]},
            {'name': 'Exercise 3', 'sets': [
                {'reps': 3, 'weight': 0, 'comment': None},
                {'reps': 4, 'weight': 0, 'comment': None},
                {'reps': 5, 'weight': 0, 'comment': None}]}]}

    response = client.post(url_for('api.workouts'), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    }, data=json.dumps(new_workout), content_type='application/json')

    assert response.status_code == 201
    json_response = json.loads(response.get_data(as_text=True))
    assert json_response['id'] == 1
    assert json_response['comment'] is None
    assert json_response['date_completed'] is None
    assert json_response['date_proposed'] == new_workout['date_proposed']
    assert json_response['exercises'] == new_workout['exercises']


def test_get_workout(client, user):
    workout = m.Workout.query.first()
    assert workout is not None

    response = client.get(url_for('api.workout', id=workout.id), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    })

    assert response.status_code == 200
    json_response = json.loads(response.get_data(as_text=True))
    workout_dump = workout.dump().data
    assert workout_dump['date_proposed'] == json_response['date_proposed']
    assert workout_dump['exercises'] == json_response['exercises']

    workouts = m.Workout.query.all()
    response = client.get(url_for('api.workouts'), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    })

    assert response.status_code == 200
    json_response = json.loads(response.get_data(as_text=True))
    assert len(json_response) == len(workouts)

#
# def test_delete_workout(client, db, user, mixer):
#     workout = m.Workout.query.order_by(m.Workout.date_proposed.desc()).first()
#     assert workout is not None
#     response = client.delete(url_for('api.workout', id=workout.id), headers={
#         'Authorization': 'Bearer ' + user.generate_token()
#     })
#
#     assert response.status_code == 204
#     assert response.content_type == 'application/json'
#     assert str(response.data) == "b''"
#     assert m.Workout.query.get(workout.id) is None
#
#
# def test_patch_workout(client, db, user, mixer):
#     workout = m.Workout.query.order_by(m.Workout.date_proposed.desc()).first()
#     assert workout is not None
#     data = workout.dump().data
#
#     # TODO figure out how to test dates.. mock db for this test?
#     data['date_completed'] = None
#     data['date_proposed'] = None
#
#     for exercise in data['exercises']:
#         for exercise_set in exercise['sets']:
#             exercise_set['weight'] = 100
#             exercise_set['comment'] = 'Good'
#
#     response = client.patch(url_for('api.workout', id=workout.id), headers={
#         'Authorization': 'Bearer ' + user.generate_token()
#     }, data=json.dumps(data), content_type='application/json')
#
#     assert response.status_code == 200
#     update = json.loads(response.get_data(as_text=True))
#     print(update)
