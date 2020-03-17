from stronk import db
from stronk.models.workout_exercise import WorkoutExercise
from stronk.models.workout import Workout
from stronk.models.exercise import Exercise

class WorkoutExerciseSuperSets(db.Model):
    src_workout_id = db.Column(db.Integer,
                               db.ForeignKey('workout.id'),
                               primary_key=True,
                               index=True,
                               nullable=False)
    src_exercise_id = db.Column(db.Integer,
                                db.ForeignKey('exercise.id'),
                                primary_key=True,
                                index=True,
                                nullable=False)
    super_set_exercise_id = db.Column(db.Integer,
                                      db.ForeignKey('exercise.id'),
                                      primary_key=True,
                                      index=True,
                                      nullable=False)

    def to_dict(self):
        """Returns a dictionary representing the attributes of the
        WorkoutExercise. Key is the name of the attribute and value is the
        value of the attribute."""
        return {
            "workout_exercise": self.get_workout_exercise().to_dict(),
            "exercise": self.get_super_set().to_dict()
        }

    def get_workout_exercise(self):
        """Returns WorkoutExercise object for the workout exercise of the
           WorkoutExerciseSuperSets. """
        res = WorkoutExercise.query.filter_by(workout_id=self.src_workout_id,
                                               exercise_id=self.src_exercise_id)
        if res:
            return res
        raise NoResultFound('WorkoutExercise does not exist.')

    def get_super_set(self):
        """Returns WorkoutExercise object for the super set of the
           WorkoutExerciseSuperSets. """
        res = WorkoutExercise.query.filter_by(workout_id=self.src_workout_id,
                                               exercise_id=self.super_set_exercise_id)
        if res:
            return res
        raise NoResultFound('WorkoutExercise does not exist.')


    def update(self, attrs):
      """Updates model given attrs.

      Params:
          attrs: Dictionary containing attributes to update. Key is the 
                  attribute name and value is the new value.
      """
      if attrs.get('src_workout_id'):
        new_id = attrs.get('src_workout_id')
        if not Workout.query.filter_by(id=new_id):
            raise NoResultFound('Workout ID does not exist')
        self.src_workout_id = new_id

      if attrs.get('src_exercise_id'):
        new_id = attrs.get('src_exercise_id')
        if not Exercise.query.filter_by(id=new_id):
          raise NoResultFound('Exercise ID does not exist')
        self.src_exercise_id = new_id
        
      if attrs.get('super_set_exercise_id'):
        new_id = attrs.get('super_set_exercise_id')
        if not Exercise.query.filter_by(id=new_id):
          raise NoResultFound('Exercise ID does not exist')

        if not WorkoutExercise.query.filter_by(workout_id=self.src_workout_id,
                                               exercise_id=new_id):
          raise NoResultFound('WorkoutExercise does not exist.')
        self.super_set_exercise_id = new_id
  