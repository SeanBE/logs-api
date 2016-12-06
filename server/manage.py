from app import create_app
from app.database import db

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from mixer.backend.sqlalchemy import Mixer

app = create_app()
manager = Manager(app)

@manager.command
def setup_db():
    db.drop_all()
    db.create_all()

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
