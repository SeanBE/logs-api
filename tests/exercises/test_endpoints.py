import json
import pytest
from flask import url_for
from pytest_factoryboy import register

from app.models.exercise import Exercise
from tests.factories import ExerciseFactory

register(ExerciseFactory)
register(ExerciseFactory, 'another_exercise')


@pytest.mark.parametrize("exercise__name", ["Some Exercise"])
@pytest.mark.parametrize("another_exercise__name", ["Another Exercise"])
def test_get_exercises(client, user, exercise, another_exercise):
    response = client.get(url_for('api.exercises'), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    })

    assert response.status_code == 200
    exercises = json.loads(response.get_data(as_text=True))

    names = [ex['name'] for ex in exercises]
    assert 'Some Exercise' in names
    assert 'Another Exercise' in names


def test_post_exercise(client, user):

    new_exercise = {'name': 'New Exercise'}
    response = client.post(url_for('api.exercises'), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    }, data=json.dumps(new_exercise), content_type='application/json')

    assert response.status_code == 201
    json_response = json.loads(response.get_data(as_text=True))
    assert new_exercise['name'] == json_response['name']

    print(json_response)
    exercise = Exercise.query.filter_by(name=new_exercise['name']).first()
    assert exercise.id == json_response['id']


def test_patch_exercise(client, user, exercise):
    updated_name = 'Version 2'
    update_data = {'name': updated_name}

    response = client.patch(url_for('api.exercise', id=exercise.id), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    }, data=json.dumps(update_data), content_type='application/json')

    assert response.status_code == 200
    json_response = json.loads(response.get_data(as_text=True))
    assert exercise.id == json_response['id']
    assert updated_name == json_response['name']


def test_get_exercise(client, user, exercise):

    response = client.get(url_for('api.exercise', id=exercise.id), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    })

    assert response.status_code == 200
    json_response = json.loads(response.get_data(as_text=True))
    assert json_response['id'] == exercise.id
    assert json_response['name'] == exercise.name


def test_delete_exercise(client, user, exercise):

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
