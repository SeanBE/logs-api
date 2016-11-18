from . import db
from .models import Workout
from .schemas import WorkoutSchema
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError


WorkoutSerializer = WorkoutSchema()

class DatabaseService(object):

    def get_list(self):
        """
        Returns list of workouts.
        """
        # TODO use offsets, limits, etc.
        workouts = Workout.query.all()
        data, errors = WorkoutSerializer.dump(workouts, many=True)

        if errors:
            print errors
            return None, errors

        return data, None

    def get(self, id):
        """
        Returns workout with id <id>.
        """

        workout = Workout.query.filter_by(id=id).first()
        data, errors = WorkoutSerializer.dump(workout)

        if errors:
            print errors
            return None, errors

        return data, None

    def create(self, data):
        """
        Creates workout.
        """

        # TODO Sort out errors.
        workout, errors = WorkoutSerializer.load(data)

        if errors:
            return False, errors

        db.session.add(workout)
        db.session.commit()

        if workout.id is not None:
            return True, None

        return False, None


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

        #TODO validate with serializer.

        workout = Workout.query.get(id)

        try:
            data1 =  {k:v for k,v in data.items() if k != 'exercises'}

            for key, value in data1.iteritems():
                setattr(workout, key, value)

            data = WorkoutSerializer.fix_exercise_entries(data)

            for new_ex, exercise in zip(data['exercises'], workout.exercises):
                # print new_ex
                # print exercise

                new_ex['exercise_name'] = new_ex.pop('exercise')
                for key, value in new_ex.iteritems():
                    setattr(exercise, key, value)

            db.session.commit()

            # Assume get request just works.
            data, _ = self.get(id)

            return data, {}

        except ValidationError as err:
                return None, {"error": err.messages}

        except SQLAlchemyError as e:
                db.session.rollback()
                return None, {"error": str(e)}
