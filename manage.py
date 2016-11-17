from app import create_app
from app.database import db

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app()

manager = Manager(app)
migrate = Migrate(app, db)

# TODO does host='0.0.0.0'?

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
