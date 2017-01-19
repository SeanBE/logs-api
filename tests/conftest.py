import pytest
import sqlite3
from sqlalchemy import event
from flask_sqlalchemy import SignallingSession

from app import create_app
from app.extensions import db as _db

import app.models as models
import tests.factories as f


FUNC_MAP = {}


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


@pytest.yield_fixture(scope='session')
def db(app):
    """Session-wide test database."""

    _db.app = app
    _db.session.remove()
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture
def user():
    user_data = {'username': 'admin', 'password': 'password'}
    user, errors = models.User.load(user_data)
    user.save()
    return user


@pytest.fixture
def workout():
    return create_workout()


@pytest.fixture
def workouts(request):
    print(request.param)
    return [create_workout() for _ in range(request.param)]


def create_workout():
    entries = []
    for _ in range(3):
        sets = f.SetEntryFactory.build_batch(3)
        entry = f.ExerciseEntryFactory.build(sets=sets)
        entries.append(entry)
    workout = f.WorkoutFactory.build(exercises=entries)
    return workout.save()

@pytest.yield_fixture
def client(app):
    """
    Setup an app client, this gets executed for each test function.

    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()


@pytest.fixture(scope='session', autouse=True)
def setup(db, app):
    # From
    # https://github.com/fastlineaustralia/cudless-testing/blob/master/tests/conftest.py
    event.listen(_db.engine, 'connect', _do_connect)
    event.listen(_db.engine, 'begin', _do_begin)
    with app.test_request_context():
        # Create nesting to prevent any commits/rollbacks within the DB
        # setup to apply onto our top level transaction.
        _db.session.begin_nested()
        # TODO. Change SignallingSession to sa.session once
        # https://github.com/mitsuhiko/flask-sqlalchemy/pull/364 is in a
        # release.
        event.listen(
            SignallingSession,
            'after_transaction_end',
            _get_restart_savepoint_func(2)
        )

        # TODO. Change SignallingSession to sa.session once
        # https://github.com/mitsuhiko/flask-sqlalchemy/pull/364 is in a
        # release.
        event.remove(
            SignallingSession,
            'after_transaction_end',
            _get_restart_savepoint_func(2)
        )
        # End our nesting for DB setup.
        _db.session.commit()

        yield

        # Our final rollback so that we end our test session without
        # leaving any DML traces in the DB.
        _db.session.rollback()


@pytest.fixture(autouse=True)
def nest_for_test(db):
    # Nesting level 1 to rollback current test.
    _db.session.begin_nested()

    # Nesting level 2 to handle any commits/rollbacks within a test.
    _db.session.begin_nested()
    # TODO. Change SignallingSession to sa.session once
    # https://github.com/mitsuhiko/flask-sqlalchemy/pull/364 is in a
    # release.
    event.listen(
        SignallingSession,
        'after_transaction_end',
        _get_restart_savepoint_func(3)
    )

    yield

    # TODO. Change SignallingSession to sa.session once
    # https://github.com/mitsuhiko/flask-sqlalchemy/pull/364 is in a
    # release.
    event.remove(
        SignallingSession,
        'after_transaction_end',
        _get_restart_savepoint_func(3)
    )
    # Rollback nesting level 2.
    _db.session.rollback()

    # Rollback nesting level 1.
    _db.session.rollback()


def _get_restart_savepoint_func(parent_levels):
    def restart_savepoint(session, transaction):
        node = transaction
        # Ensure we're at the proper nesting level.
        for i in range(parent_levels):
            node = node.parent
        if node is None:
            session.expire_all()
            session.begin_nested()

    # We can't generate a function on the fly on every function call
    # since SQLAlchemy's `event.remove` will look for the same function
    # object which was previously added by `event.listen`. Hence we use
    # a dict to save each generated function only once, and recall it
    # from the dict later when `event.remove` is called.
    return FUNC_MAP.setdefault(parent_levels, restart_savepoint)


def _do_connect(dbapi_connection, connection_record):
    '''See `this explanation`__ what this is needed for.

    __ http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl
    '''
    if isinstance(dbapi_connection, sqlite3.Connection):
        # Disable pysqlite's emitting of the BEGIN statement entirely.
        # Also stops it from emitting COMMIT before any DDL.
        dbapi_connection.isolation_level = None


def _do_begin(conn):
    '''See `this explanation`__ what this is needed for.

    __ http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl
    '''
    if isinstance(conn.connection.connection, sqlite3.Connection):
        # Emit our own BEGIN.
        conn.execute('BEGIN')
