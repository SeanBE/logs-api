import json
import pytest
from flask import jsonify, url_for
from app.models.exercise import Exercise


def test_get_exercises(client, db, user):
    exercise_name = 'Bench Press'
    exercise, errors = Exercise.load({'name': exercise_name})
    exercise.save()

    response = client.get(url_for('api.exercises'), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    })

    assert response.status_code == 200
    exercises = json.loads(response.get_data(as_text=True))
    assert exercise_name in [ex['name'] for ex in exercises]


def test_post_exercise(client, db, user):

    new_exercise = {'name': 'New Exercise'}
    response = client.post(url_for('api.exercises'), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    }, data=json.dumps(new_exercise), content_type='application/json')

    assert response.status_code == 201
    json_response = json.loads(response.get_data(as_text=True))
    assert new_exercise['name'] == json_response['name']

    exercise = Exercise.query.filter_by(name=new_exercise['name']).first()
    assert exercise.id == json_response['id']



def test_patch_exercise(client, db, user):
    updated_name = 'Version 2'
    exercise, errors = Exercise.load({'name': 'Version 1'})
    exercise.save()

    response = client.patch(url_for('api.exercise', id=exercise.id), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    }, data=json.dumps({'name': updated_name}), content_type='application/json')

    assert response.status_code == 200
    update = json.loads(response.get_data(as_text=True))
    assert updated_name == update['name']
    assert exercise.id == update['id']


def test_get_exercise(client, db, user):
    exercise_name = 'Another Exercise'
    exercise, errors = Exercise.load({'name': exercise_name})
    exercise.save()

    response = client.get(url_for('api.exercise', id=exercise.id), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    })

    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert data['id'] == exercise.id
    assert data['name'] == exercise_name


def test_delete_exercise(client, db, user):
    name = 'Exercise to be deleted'
    exercise, errors = Exercise.load({'name': name})
    exercise.save()

    response = client.delete(url_for('api.exercise', id=exercise.id), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    })

    assert response.status_code == 204
    assert response.content_type == 'application/json'
    assert str(response.data) == "b''"
    assert Exercise.query.get(exercise.id) is None


def test_put_exercises(client):
    response = client.put(url_for('api.exercises'))
    assert response.status_code == 405
    assert response.content_type == 'application/json'
    assert b'The method is not allowed for the requested URL.' in response.data
