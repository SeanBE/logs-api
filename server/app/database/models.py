from . import db
from datetime import datetime


class Workout(db.Model):
    __tablename__ = 'workout'

    id = db.Column(db.Integer, primary_key=True)

    date_proposed = db.Column(db.Date, nullable=False)
    date_completed = db.Column(db.Date)
    date_created = db.Column(db.DateTime, nullable=False)
    exercises = db.relationship('ExerciseEntry', cascade = "all,delete", backref=db.backref('workout'), lazy='joined', order_by=('ExerciseEntry.exercise_id'))

    def __init__(self, date_proposed, exercises=None, date_completed=None, date_created=None):

        self.exercises = exercises or []
        self.date_completed = date_completed
        self.date_proposed = date_proposed

        if date_created is None:
            self.date_created = datetime.utcnow()

    def __repr__(self):
        return '<Workout {} has {} exercises.>'.format(self.date_proposed, len(self.exercises))


class ExerciseEntry(db.Model):
    __table__name = 'exercise_entry'
    __table_args__ = (db.UniqueConstraint('set_num', 'exercise_id', 'workout_id',
            name='_exercise_set_workout_uc'),)

    id = db.Column(db.Integer, primary_key=True)

    set_num = db.Column(db.Integer, nullable=False)

    exercise = db.relationship('Exercise')
    exercise_id = db.Column (db.Integer, db.ForeignKey('exercise.id'), nullable=False)

    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)

    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    def __init__(self, exercise_name, set_num, reps, weight, comment=None):

        self.exercise = Exercise.query.filter_by(name=exercise_name).first()
        self.exercise_id = self.exercise.id

        self.set_num = set_num
        self.reps = reps
        self.weight = weight
        self.comment = comment

    def __repr__(self):
        return '<Exercise Entry {} set {} reps {} weight {} comment {}>'.format(self.exercise_id, self.set_num, self.reps, self.weight, self.comment)


class Exercise(db.Model):
    __tablename__ = 'exercise'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}, ({})>'.format(self.id, self.name)
