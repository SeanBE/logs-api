from . import mongo, psql

class WorkoutService(object):

    def __init__(self, mongo, psql):
        self.mongo = mongo
        self.psql = psql

    def all(self):
        return self.mongo.db.workouts.find()


    def get(self, name, date):
        return self.mongo.db.workouts.find_one({'username': name, 'date_proposed': date})


    def delete(self, name, date):
        from models import Workout

        self.mongo.db.workouts.delete_one({'username': name, 'date_proposed': date})

        # TODO first?
        self.psql.session.delete(Workoutself.query.filter_by(username=name, date_proposed=date))
        self.psql.session.commit()


    def create(self, data):

        # TODO huh??
        from models import Workout, Exercise, ExerciseEntry

        workout = Workout(data['username'], data['date_proposed'])
        for e in data['exercises']:
            exercise = Exercise.query.filter_by(name=e['name'])

            for idx, s in enumerate(e['sets']):
                entry = ExerciseEntry(exercise, idx, s['reps'], s['weight'], s['comment'])
                workout.exercises.append(entry)

        self.psql.session.add(workout)
        self.psql.session.commit()

        self.mongo.db.workouts.insert_one(data)


    def update(self, name, date, data):
        from models import Workout, Exercise, ExerciseEntry

        workout = Workout.query.filter_by(username=name, date_proposed=date)

        if workout:
            workout.name = data['name']
            workout.date_completed = data['date_completed']
            workout.exercises = []

            for e in data['exercises']:
                exercise = Exercise.query.filter_by(name=e['name'])

                for idx, s in enumerate(e['sets']):
                    entry = ExerciseEntry(exercise, idx, s['reps'], s['weight'], s['comment'])
                    workout.exercises.append(entry)

        self.psql.session.commit()

        self.mongo.db.workouts.replace_one({'username': name, 'date_proposed': date}, data)


service = WorkoutService(mongo, psql)
