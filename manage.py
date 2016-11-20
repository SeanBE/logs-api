from app import create_app,config
from app.database import db

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app(config.ProdConfig)

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
