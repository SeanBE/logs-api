import datetime as dt
from flask_script import Manager, Shell
from mixer.backend.flask import Mixer
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.extensions import db
from app import models

app = create_app()
manager = Manager(app)

# TODO gunicorn command (with loglevel/reload params)
#  /usr/local/bin/gunicorn -reload --log-level DEBUG -w 4 -b 0.0.0.0:8001 wsgi:app

@manager.command
def setup_db():
    db.drop_all()
    db.create_all()

    models.User.load({'username': 'admin', 'password': 'QDZFuq3g54ZRGwdt'}).save()

# TODO test and lint.
# @manager.command
# def test():
#     """Runs unit tests."""
#     tests = subprocess.call(['python', '-c', 'import tests; tests.run()'])
#     sys.exit(tests)
#
#
# @manager.command
# def lint():
#     """Runs code linter."""
#     lint = subprocess.call(['flake8', '--ignore=E402', 'flack/',
#                             'manage.py', 'tests/']) == 0
#     if lint:
#         print('OK')
#     sys.exit(lint)


@manager.command
def fake_data():
    class MyOwnMixer(Mixer):
        # Custom Mixer for Flask init constructors.

        def populate_target(self, values):
            target = self.__scheme(**values)
            return target

    mixer = MyOwnMixer()
    mixer.init_app(app)
    users = mixer.cycle(10).blend(models.User)
    exercises = mixer.cycle(15).blend(models.Exercise)
    entries = mixer.cycle(50).blend(models.ExerciseEntry)
    workouts = mixer.cycle(5).blend(models.Workout)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, models=models)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
