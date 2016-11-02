from . import mongo, psql

class WorkoutService(object):

    def __init__(self, mongo, psql):
        self.mongo = mongo
        self.psql = psql

    def all(self):
        # Use Mongo for retrieval.
        return self.mongo.db.workouts.find()


    def get(self, id):
        # Use Mongo for retrieval.
        return mongo.db.workouts.find_one({'id': id})


    def delete(self, username, date):
        from models import Workout

        self.mongo.db.workouts.delete_one({'username':username, 'date_completed':date})

        self.psql.session.delete(Workout.query.filter_by(username=username, date_completed=date))
        self.psql.session.commit()


    def create(self, data):
        # TODO huh??
        from models import Workout, Exercise

        workout = Workout(data['username'], data['date_completed'], data)
        for e in data['exercises']:
            for idx,s in enumerate(e['sets']):
                exercise = Exercise(e['name'], idx, s['reps'], s['weight'], s['comment'])
                workout.exercises_completed.append(exercise)

        self.psql.session.add(workout)
        self.psql.session.commit()

        self.mongo.db.workouts.insert_one(data)


    def update(self, id, data):
        from models import Workout, Exercise

        workout = Workout.query.get(id)

        if workout:
            workout.name = data['name']
            workout.date_completed = data['date_completed']
            workout.workout_json = data
            workout.exercises_completed = []

            for e in data['exercises']:
                for idx,s in enumerate(e['sets']):
                    exercise = Exercise(e['name'], idx, s['reps'], s['weight'], s['comment'])
                    workout.exercises_completed.append(exercise)

        self.psql.session.commit()
        self.mongo.db.workouts.replace_one({'id': id}, data)


service = WorkoutService(mongo, psql)
