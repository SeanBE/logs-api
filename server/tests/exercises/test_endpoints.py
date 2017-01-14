import json
import pytest
from flask import jsonify, url_for
from app.models.exercise import Exercise


def test_get_all_exercises(client, db, user):

    exercise, errors = Exercise.load({'name': 'Bench Press'})
    assert not errors
    exercise.save()

    response = client.get(url_for('api.exercises'), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    })

    assert response.status_code == 200
    exercises = json.loads(response.get_data(as_text=True))
    assert 'Bench Press' in [ex['name'] for ex in exercises]


def test_put_exercises(client):
    response = client.put(url_for('api.exercises'))
    assert response.status_code == 405
    assert response.content_type == 'application/json'
    assert b'The method is not allowed for the requested URL.' in response.data
