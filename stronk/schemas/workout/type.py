import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from stronk.models.workout import Workout as WorkoutModel
from stronk.models.workout_exercise import WorkoutExercise as WorkoutExerciseModel

from stronk.schemas.workout_exercise.type import WorkoutExercise

class Workout(SQLAlchemyObjectType):
    class Meta:
        model = WorkoutModel

    workout_exercises = graphene.List(WorkoutExercise)
    
    def resolve_workout_exercises(parent, info):
        # root is the workout model
        return WorkoutExerciseModel.find_workout_exercises(workout_id = parent.id)