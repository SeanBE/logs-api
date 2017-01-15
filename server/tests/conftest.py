import os
import pytest
from mixer.backend.flask import Mixer

import app.models as m
from app import create_app
from app.config import TestConfig
from app.extensions import db as _db


@pytest.yield_fixture(scope='session')
def app():
    """
    Setup our flask test app, this only gets executed once.

    :return: Flask app
    """
    _app = create_app('testing')

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.yield_fixture(scope='function')
def client(app):
    """
    Setup an app client, this gets executed for each test function.

    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()


@pytest.yield_fixture(scope='session')
def db(app):
    """Session-wide test database."""
    if os.path.exists(TestConfig.DB_PATH):
        os.unlink(TestConfig.DB_PATH)

    _db.app = app
    _db.session.remove()
    _db.create_all()

    yield _db

    _db.drop_all()
    os.unlink(TestConfig.DB_PATH)


@pytest.yield_fixture(scope='session')
def mixer(app):
    class MyOwnMixer(Mixer):
        # Custom Mixer for Flask init constructors.

        def populate_target(self, values):
            target = self.__scheme(**values)
            return target

    mixer = MyOwnMixer()
    mixer.init_app(app)
    users = mixer.cycle(5).blend(m.User)
    exercises = mixer.cycle(10).blend(m.Exercise)
    entries = mixer.cycle(6).blend(m.ExerciseEntry)
    workouts = mixer.cycle(3).blend(m.Workout)


@pytest.fixture(scope='session')
def user(db):
    # TODO do we need db as param to link dependency?
    user, errors = m.User.load({'username': 'admin', 'password': 'password'})
    assert not errors
    user.save()
    return user
