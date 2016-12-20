from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.database.models import Workout, Exercise, ExerciseEntry
