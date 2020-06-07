from sqlalchemy.exc import DBAPIError

from stronk import db
from stronk.constants import DATABASE_ERROR_MSG
from stronk.models.exercise import Exercise
from stronk.models.workout import Workout

from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm.exc import NoResultFound

from stronk.errors.unexpected_error import UnexpectedError

class WorkoutExercise(db.Model):
    workout_id = db.Column(db.Integer,
                           db.ForeignKey('workout.id'),
                           primary_key=True,
                           index=True,
                           nullable=False)
    exercise_id = db.Column(db.Integer,
                            db.ForeignKey('exercise.id'),
                            primary_key=True,
                            index=True,
                            nullable=False)
    workout_weights = db.Column(ARRAY(db.Float), nullable=False)
    workout_reps = db.Column(ARRAY(db.Integer), nullable=False)
    rest_time = db.Column(db.Integer, nullable=False)

    @staticmethod
    def create(program_id, workout_id, workout_weights, workout_reps, rest_time):
        TODO

    def to_dict(self):
        """Returns a dictionary representing the attributes of the
           WorkoutExercise. Key is the name of the attribute and value is the
           value of the attribute."""
        return {
            "workout": self.get_workout().to_dict(),
            "exercise": self.get_exercise().to_dict(),
            "workout_weights": self.workout_weights,
            "workout_reps": self.workout_reps,
            "rest_time": self.rest_time
        }

    def get_exercise(self):
        """Returns Exercise object for the exercise of the workoutExercise. """
        return Exercise.query.filter_by(id=self.exercise_id)

    def get_workout(self):
        """Returns Workout object for the workout of the workoutExercise. """
        return Workout.query.filter_by(id=self.workout_id)

    def update(self, attrs):
        """Updates model given attrs.

        Params:
            attrs: Dictionary containing attributes to update. Key is the 
                   attribute name and value is the new value.
        """
        if attrs.get('workout_id'):
            new_id = attrs.get('workout_id')
            if Workout.query.filter_by(id=new_id):
                self.workout_id = new_id
            else:
                raise NoResultFound('Workout ID does not exist')
        if attrs.get('exercise_id'):
            new_id = attrs.get('exercise_id')
            if Exercise.query.filter_by(id=new_id):
                self.exercise_id = new_id
            else:
                raise NoResultFound('Exercise ID does not exist')
        if attrs.get('workout_weights'):
            self.workout_weights = attrs.get('workout_weights')
        if attrs.get('workout_reps'):
            self.workout_reps = attrs.get('workout_reps')
        if attrs.get('rest_time'):
            self.rest_time = attrs.get('rest_time')

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            data = {
                "message": "Workout exercise successfully deleted."
            }
        except DBAPIError as err:
            raise UnexpectedError(DATABASE_ERROR_MSG)

    @staticmethod
    def find_workout_exercises(workout_id):
        """Returns list of workout exercises that belong to a workout with workout_id."""
        return WorkoutExercise.query.filter_by(workout_id=workout_id)

    @staticmethod
    def find_workout_exercise(workout_id, exercise_id):
        """Returns the workout exercise for a workout"""
        return WorkoutExercise.query.filter_by(workout_id=workout_id).filter_by(exercise_id=exercise_id).first
