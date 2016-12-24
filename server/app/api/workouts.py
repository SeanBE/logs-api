from flask import request
from flask_restful import Resource

from webargs import fields, validate
from webargs.flaskparser import use_kwargs

from app.auth import auth
from app.models import Workout as W


class Workout(Resource):

    decorators = [auth.login_required]

    def get(self, id):

        workout = W.query.filter_by(id=id).first()

        if workout:
            return workout.dump().data, 200

        return {"error": "Workout not found!"}, 404

    def patch(self, id):
        data = request.get_json(force=True)
        workout = W.query.filter_by(id=id).first()

        # Ignore ID and Date Created.
        data.pop('id')
        data.pop('date_created')

        exercises = []
        for key, values in data['exercises'].items():
            for entry in values:
                entry['exercise'] = key
                exercises.append(entry)
        data['exercises'] = exercises

        for new_ex, exercise in zip(data['exercises'], workout.exercises):
            new_ex['exercise_name'] = new_ex.pop('exercise')
            for key, value in new_ex.items():
                setattr(exercise, key, value)

        data.pop('exercises')

        workout.update(**data)
        return workout.dump().data, 200

    def delete(self, id):

        deleted = (W
                   .query
                   .filter_by(id=id)
                   .first()
                   .delete())

        if deleted:
            return None, 204

        return {"error": "Could not delete workout!"}, 404


class WorkoutList(Resource):

    decorators = [auth.login_required]

    page_args = {
        'limit': fields.Int(missing=5),
        'offset': fields.Int(missing=0)
    }

    @use_kwargs(page_args)
    def get(self, limit, offset):

        workout_list = (W
                        .query
                        .limit(limit)
                        .offset(offset)
                        .all())

        workouts, errors = W.dump_list(workout_list)

        return workouts, 200

    def post(self):

        data = request.get_json(force=True)
        workout = W.load(data).save()

        return workout.dump().data, 201
