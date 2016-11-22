from app import create_app,config
from app.database import db

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from mixer.backend.sqlalchemy import Mixer



app = create_app(config.DevConfig)

manager = Manager(app)


# class MyOwnMixer(Mixer):
#
#     def populate_target(self, values):
#         print values
#         target = self.__scheme(**values)
#         return target
#
# mixer = MyOwnMixer()

# @manager.command
# def setup_db():
#     from app.database.models import Workout, ExerciseEntry, Exercise
#
#     db.drop_all()
#     db.create_all()
#
#     # mixer.init_app(app)
#
#     mixer.blend(Exercise)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
