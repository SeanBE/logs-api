class BaseService(object):

    def all(self):
        pass

    def get(self, username, date):
        pass

    def create(self, data):
        pass

    def update(self, username, date, data):
        pass

    def delete(self, username, date):
        pass


class MongoService(BaseService):

    def __init__(self, mongo):
        self.mongo = mongo

    def all(self):
        return self.mongo.db.workouts.find()

    def get(self, name, date):
        return self.mongo.db.workouts.find_one({'username': name, 'date_proposed': date})

    def create(self, data):
        return self.mongo.db.workouts.insert_one(data)

    def update(self, name, date, data):
        return self.mongo.db.workouts.replace_one({'username': name, 'date_proposed': date}, data)

    def delete(self, name, date):
        return self.mongo.db.workouts.delete_one({'username': name, 'date_proposed': date})


class PostgresService(BaseService):

    def __init__(self, psql):
        self.db = psql

    def all(self):
        # from models import Workout,ExerciseEntry
        # workouts = self.psql.session.query(Workout).filter().all()
        #
        # exercise_to_json = lambda x: {
        #     "name": "bc",
        #     "sets": ""
        #
        # }
        #
        # workout_to_json = lambda x: {
        #     "date_proposed": x.date_proposed,
        #     "username": x.username,
        #     "date_completed": x.date_completed
        #     "exercises:" map(exercise_to_json, x.exercises)
        #     }
        #
        # return map(workout_to_json, workouts)
        pass

    def get(self, name, date):
        # from models import Workout
        # return self.psql.session.query(Workout).filter_by(username=name,
        # date_proposed=date).first()
        pass

    def delete(self, name, date):
        from models import Workout

        workout = self.psql.session.query(Workout).filter_by(
            username=name, date_proposed=date).first()

        if workout:
            self.psql.session.delete(workout)
            self.psql.session.commit()

    def create(self, data):
        from models import Workout, Exercise, ExerciseEntry

        workout = Workout(data['username'], data['date_proposed'])

        for e in data['exercises']:
            exercise = Exercise.query.filter_by(name=e['name']).first()

            for idx, s in enumerate(e['sets']):
                entry = ExerciseEntry(exercise, idx, s['reps'], s[
                                      'weight'], s['comment'])
                workout.exercises.append(entry)

        self.psql.session.add(workout)
        self.psql.session.commit()

    def update(self, name, date, data):
        # from models import Workout, Exercise, ExerciseEntry

        # workout = Workout.query.filter_by(username=name, date_proposed=date).first()

        # if workout:
        #     print 'Found workout!'
        #     workout.username = data['username']
        #     workout.date_proposed = data['date_proposed']
        #     workout.date_completed = data['date_completed']
        #
        #     with self.psql.session.no_autoflush:
        #
        #         workout.exercises = []
        #
        #         for e in data['exercises']:
        #             exercise = Exercise.query.filter_by(name=e['name']).first()
        #
        #             for idx, s in enumerate(e['sets']):
        #                 entry = ExerciseEntry(exercise, idx, s['reps'], s['weight'], s['comment'])
        #                 entry.workout_id = workout.id
        #                 workout.exercises.append(entry)
        #
        # self.psql.session.commit()
        pass
