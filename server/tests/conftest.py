import os
import pytest

from app import create_app
from app.models.user import User
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


@pytest.fixture(scope='session')
def user(db):
    # TODO do we need db as param to link dependency?
    user, errors = User.load({'username': 'admin', 'password': 'password'})
    assert not errors
    user.save()
    return user
