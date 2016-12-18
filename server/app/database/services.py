from . import db
from .models import Workout, Exercise
from .schemas import WorkoutSchema
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

WorkoutSerializer = WorkoutSchema()

class DatabaseService(object):

    def get_list(self, limit, offset):
        """
        Returns list of workouts.
        """
        workouts = Workout.query.limit(limit).offset(offset).all()

        data, errors = WorkoutSerializer.dump(workouts, many=True)

        if errors:
            #print errors
            return None, errors

        return data, None

    def get(self, id):
        """
        Returns workout with id <id>.
        """

        workout = Workout.query.filter_by(id=id).first()
        data, errors = WorkoutSerializer.dump(workout)

        if errors:
            #print errors
            return None, errors

        return data, None

    def create(self, data):
        """
        Creates workout.
        """

        # TODO Sort out errors.
        # Validation process?
        workout, errors = WorkoutSerializer.load(data)
        if errors:
            return None, errors

        db.session.add(workout)
        db.session.commit()

        new_workout, _ = self.get(workout.id)

        return new_workout, None

    def delete(self, id):
        """
        Deletes workout with id <id>.
        """
        workout = Workout.query.get(id)

        try:
            db.session.delete(workout)
            db.session.commit()
            return {}

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}

    def update(self, id, data):
        """
        Update workout with id <id> using data <data>.
        """

        # TODO validate with serializer.

        workout = Workout.query.get(id)

        try:
            data1 = {k: v for k, v in data.items() if k != 'exercises'}

            for key, value in data1.iteritems():
                setattr(workout, key, value)

            data = WorkoutSerializer.fix_exercise_entries(data)

            for new_ex, exercise in zip(data['exercises'], workout.exercises):
                new_ex['exercise_name'] = new_ex.pop('exercise')
                for key, value in new_ex.iteritems():
                    setattr(exercise, key, value)

            db.session.commit()

            data, _ = self.get(id)

            return data, {}

        except ValidationError as err:
            return None, {"error": err.messages}

        except SQLAlchemyError as e:
            db.session.rollback()
            return None, {"error": str(e)}
