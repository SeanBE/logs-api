import sys
import subprocess
import datetime as dt
from flask_script import Manager, Shell
from mixer.backend.flask import Mixer
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.extensions import db
from app import models

app = create_app()
manager = Manager(app)


@manager.command
def setup_db():
    db.drop_all()
    db.create_all()

    user_data = {'username': 'admin', 'password': 'QDZFuq3g54ZRGwdt'}
    models.User.load(user_data).data.save()


@manager.command
def test():
    tests = subprocess.call(['py.test'])
    sys.exit(tests)


@manager.command
def lint():
    lint = subprocess.call(['flake8', '--ignore=E402', 'app/',
                            'manage.py', 'tests/']) == 0
    if lint:
        print('OK')
    sys.exit(lint)


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
