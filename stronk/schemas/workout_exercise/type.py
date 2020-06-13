import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from stronk.models.workout_exercise import WorkoutExercise as WorkoutExerciseModel
from stronk.models.exercise import Exercise as ExerciseModel

from stronk.schemas.exercise.type import Exercise

class WorkoutExercise(SQLAlchemyObjectType):
    class Meta:
        model = WorkoutExerciseModel

    exercise = graphene.Field(Exercise)

    def resolve_exercise(parent: WorkoutExerciseModel, info):
        # root is the workout model
        return ExerciseModel.find_by_id(id=parent.exercise_id)