from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy

mongo = PyMongo()
psql = SQLAlchemy()

from .models import Workout, Exercise, ExerciseEntry
from .services import MongoService, PostgresService

mongo_service = MongoService(mongo)
psql_service = PostgresService(psql)
