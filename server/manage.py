import datetime as dt
from flask_script import Manager
from mixer.backend.flask import Mixer
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app.extensions import db
from app.models import User, Exercise, ExerciseEntry, Workout

app = create_app()
manager = Manager(app)


class MyOwnMixer(Mixer):
    # Custom Mixer for Flask init constructors.

    def populate_target(self, values):
        target = self.__scheme(**values)
        return target


@manager.command
def setup_db():
    db.drop_all()
    db.create_all()

    user = User.create({'username': 'sean', 'password': 'test'})
    db.session.add(user)
    db.session.commit()


@manager.command
def fake_data():
    mixer = MyOwnMixer()
    mixer.init_app(app)
    users = mixer.cycle(10).blend(User)
    exercises = mixer.cycle(15).blend(Exercise)
    entries = mixer.cycle(50).blend(ExerciseEntry)
    workouts = mixer.cycle(20).blend(Workout)


migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
