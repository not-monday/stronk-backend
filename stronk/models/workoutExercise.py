from stronk import db
from stronk.models.exercise import Exercise
from stronk.models.workout import Workout

from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm.exc import NoResultFound

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
            if Workout.query.filter_by(id=self.workout_id):
                self.workout_id = attrs.get('workout_id')
            else:
                raise NoResultFound('Workout ID does not exist')
        if attrs.get('exercise_id'):
            if Exercise.query.filter_by(id=self.exercise_id):
                self.exercise_id = attrs.get('exercise_id')
            else:
                raise NoResultFound('Exercise ID does not exist')
        if attrs.get('workout_weights'):
            self.workout_weights = attrs.get('workout_weights')
        if attrs.get('workout_reps'):
            self.workout_reps = attrs.get('workout_reps')
        if attrs.get('rest_time'):
            self.rest_time = attrs.get('rest_time')
