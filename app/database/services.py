from . import db
from .models import Workout
from .schemas import WorkoutSchema
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError


WorkoutSerializer = WorkoutSchema()

class DatabaseService(object):

    def get_list(self):
        workouts = Workout.query.all()
        data, errors = WorkoutSerializer.dump(workouts, many=True)

        if errors:
            # TODO report errors.
            print errors

        return data

    def get(self, id):
        workout = Workout.query.filter_by(id=id).first()
        data, errors = WorkoutSerializer.dump(workout)

        if errors:
            # TODO report errors.
            print errors

        return data

    def create(self, data):
        # TODO send errors??
        workout = WorkoutSerializer.load(data).data
        db.session.add(workout)
        db.session.commit()

    def delete(self, id):
        workout = Workout.query.get(id)

        try:
            db.session.delete(workout)
            db.session.commit()
            return None, {}

        except SQLAlchemyError as e:
            db.session.rollback()
            return None, jsonify({"error": str(e)})

    def update(self, id, data):

        workout = Workout.query.get(id)
        print workout
        print data
        #TODO validate with serializer.
        try:
            data1 =  {k:v for k,v in data.items() if k != 'exercises'}

            for key, value in data1.iteritems():
                setattr(workout, key, value)

            data = WorkoutSerializer.fix_exercise_entries(data)

            for new_ex, exercise in zip(data['exercises'], workout.exercises):
                new_ex['exercise_name'] = new_ex.pop('exercise')
                for key, value in new_ex.iteritems():
                    setattr(exercise, key, value)

            db.session.commit()
            return self.get(id), {}

        except ValidationError as err:
                return None, {"error": err.messages}

        except SQLAlchemyError as e:
                db.session.rollback()
                return None, {"error": str(e)}
