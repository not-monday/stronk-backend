import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from stronk.models.exercise import Exercise as ExerciseModel
from stronk.models.workout_exercise import WorkoutExercise as WorkoutExerciseModel

class Exercise(SQLAlchemyObjectType):
    class Meta:
        model = ExerciseModel


class WorkoutExercise(SQLAlchemyObjectType):
    class Meta:
        model = WorkoutExerciseModel

    exercise = graphene.Field(Exercise)

    def resolve_exercise(root, info):
        return ExerciseModel.find_by_id(root.exercise_id)