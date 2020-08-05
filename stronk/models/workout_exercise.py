from sqlalchemy.exc import DBAPIError

from stronk import db
from stronk.constants import DATABASE_ERROR_MSG
from stronk.models.exercise import Exercise
from stronk.models.workout import Workout

from stronk.errors.unexpected_error import UnexpectedError
from stronk.errors.conflict import Conflict
from stronk.errors.bad_attributes import BadAttributes

from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm.exc import NoResultFound

from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from sqlalchemy.exc import DBAPIError, IntegrityError

MISMATCHED_LENGTHS_ERROR_MSG = "Number of weights needs to be the same as the number of reps"


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
    superset_exercise_id = db.Column(db.Integer,
                                      db.ForeignKey('exercise.id'),
                                      primary_key=False,
                                      index=True)
    workout_weights = db.Column(ARRAY(db.Float), nullable=False)
    workout_reps = db.Column(ARRAY(db.Integer), nullable=False)
    rest_time = db.Column(db.Integer, nullable=False)

    @staticmethod
    def create(workout_id, exercise_id, superset_exercise_id, workout_weights, workout_reps, rest_time):
        workoutExercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            superset_exercise_id=superset_exercise_id,
            workout_weights=workout_weights,
            workout_reps=workout_reps,
            rest_time=rest_time if rest_time else 0
        )

        if (len(workout_weights) != len(workout_reps)):
            raise BadAttributes(MISMATCHED_LENGTHS_ERROR_MSG)

        try:
            db.session.add(workoutExercise)
            db.session.commit()

            return workoutExercise
        except IntegrityError as err:
            if isinstance(err.orig, UniqueViolation):
                raise Conflict(
                    "Exercise has already been added to this workout")
            elif isinstance(err.orig, ForeignKeyViolation):
                raise BadAttributes("Workout or exercise not found")
            else:
                raise UnexpectedError(DATABASE_ERROR_MSG)
        except DBAPIError as err:
            raise UnexpectedError(DATABASE_ERROR_MSG)

    def to_dict(self):
        """Returns a dictionary representing the attributes of the
           WorkoutExercise. Key is the name of the attribute and value is the
           value of the attribute."""
        return {
            "workout": self.get_workout().to_dict(),
            "exercise": self.get_exercise().to_dict(),
            "superset_exercise_id": self.get_superset_exercise().to_dict(),
            "workout_weights": self.workout_weights,
            "workout_reps": self.workout_reps,
            "rest_time": self.rest_time
        }

    def get_exercise(self):
        """Returns Exercise object for the exercise of the workoutExercise. """
        return Exercise.query.filter_by(id=self.exercise_id)

    def get_superset_exercise(self):
        """Returns excercise object for the super set of the WorkoutExercise"""
        return Exercise.query.filter_by(id=self.superset_exercise_id)


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

        if attrs.get('superset_exercise_id'):
            new_superset_id = attrs.get('superset_exercise_id')
            if Exercise.query.filter_by(id=new_superset_id):
                self.superset_exercise_id = new_superset_id
            else:
                raise NoResultFound('Superset exercise ID does not exist')  

        newWorkoutsWeights = attrs.get('workout_weights')
        newWorkoutReps = attrs.get('workout_reps')
       
        # check if the list of new workout weights and list of reps have the same length
        newWorkoutWeightsLen = len(
            newWorkoutsWeights) if newWorkoutsWeights else len(self.workout_weights)
        newWorkoutRepsLen = len(
            newWorkoutReps) if newWorkoutReps else len(self.workout_reps)

        if newWorkoutWeightsLen != newWorkoutRepsLen:
            raise BadAttributes(MISMATCHED_LENGTHS_ERROR_MSG)

        if newWorkoutsWeights:
            self.workout_weights = newWorkoutsWeights
        if newWorkoutReps:
            self.workout_reps = newWorkoutReps

        if attrs.get('rest_time'):
            self.rest_time = attrs.get('rest_time')

    def removeSuperSet(self):
        self.superset_exercise_id = None

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            data = {
                "message": "Workout exercise successfully deleted."
            }
        except DBAPIError as err:
            raise UnexpectedError(DATABASE_ERROR_MSG)

    def clone(self, new_workout_id: int):
        return WorkoutExercise.create(
                    workout_id=new_workout_id, 
                    exercise_id=self.exercise_id, 
                    superset_exercise_id=self.superset_exercise_id, 
                    workout_weights=self.workout_weights, 
                    workout_reps=self.workout_reps, 
                    rest_time=self.rest_time
                )

    @staticmethod
    def deleteWorkoutExercises(workout_id):
        """deletes all workout exercises associated with a workout"""
        workoutExercises = WorkoutExercise.find_workout_exercises(workout_id)
        for workoutExercise in workoutExercises:
            workoutExercise.delete()

    @staticmethod
    def find_workout_exercises(workout_id):
        """Returns list of workout exercises that belong to a workout with workout_id."""
        return WorkoutExercise.query.filter_by(workout_id=workout_id)

    @staticmethod
    def find_workout_exercise(workout_id, exercise_id):
        """Returns the workout exercise for a workout"""
        return WorkoutExercise.query.filter_by(workout_id=workout_id).filter_by(exercise_id=exercise_id).first()
