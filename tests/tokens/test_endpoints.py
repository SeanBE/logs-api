import pytest
import base64
from flask import jsonify, url_for
from app.models.user import User


def test_get_token(client):
    response = client.get(url_for('api.tokens'))
    assert response.status_code == 405
    assert response.content_type == 'application/json'
    assert b'The method is not allowed for the requested URL.' in response.data


def test_put_token(client):
    response = client.put(url_for('api.tokens'))
    assert response.status_code == 405
    assert response.content_type == 'application/json'
    assert b'The method is not allowed for the requested URL.' in response.data


def test_patch_token(client):
    response = client.patch(url_for('api.tokens'))
    assert response.status_code == 405
    assert response.content_type == 'application/json'
    assert b'The method is not allowed for the requested URL.' in response.data


def test_delete_token(client, db, user):
    response = client.delete(url_for('api.tokens'), headers={
        'Authorization': 'Bearer ' + user.generate_token()
    })
    assert response.status_code == 204
    assert response.content_type == 'application/json'
    assert str(response.data) == "b''"


def test_post_token(client, db):
    username = 'abc'
    password = 'def'
    user = persist_user(username, password)

    b64encoded = base64.b64encode(bytes(username + ":" + password, 'ascii'))
    response = client.post(url_for('api.tokens'), headers={
        'Authorization': 'Basic ' + b64encoded.decode('ascii')
    })

    assert response.status_code == 200
    assert response.content_type == 'application/json'
    savedToken = User.query.filter_by(username=username).first().token
    assert bytes(savedToken, "ascii") in response.data


def persist_user(username, password):
    user, errors = User.load({'username': username, 'password': password})
    assert not errors
    user.save()
    return user
