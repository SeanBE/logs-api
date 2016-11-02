from . import psql as db
from datetime import datetime

class Workout(db.Model):
    __tablename__ = 'workout'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String) # TODO multiple users.

    date_proposed = db.Column(db.Date, nullable=False)
    date_completed = db.Column(db.Date)
    date_created = db.Column(db.DateTime, nullable=False)

    exercises = db.relationship('ExerciseEntry', cascade = "all,delete", backref=db.backref('workout'), lazy='joined')

    def __init__(self, username, date_proposed, date_created=None):
        self.username = username

        self.date_completed = None
        self.date_proposed = date_proposed
        if date_created is None:
            self.date_created = datetime.utcnow()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class ExerciseEntry(db.Model):
    __table__name = 'exercise_entry'
    __table_args__ = (db.UniqueConstraint('set_num', 'exercise_id', 'workout_id',
            name='_exercise_set_workout_uc'),)

    id = db.Column(db.Integer, primary_key=True)

    # Unique constraint on these three.
    set_num = db.Column(db.Integer, nullable=False)

    exercise = db.relationship('Exercise')
    exercise_id = db.Column (db.Integer, db.ForeignKey('exercise.id'), nullable=False)

    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)

    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    def __init__(self, exercise, set_num, reps, weight, comment=None):
        self.exercise = exercise
        self.exercise_id = exercise.id

        self.set_num = set_num
        self.reps = reps
        self.weight = weight
        self.comment = comment

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Exercise(db.Model):
    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}, ({})>'.format(self.id, self.name)
