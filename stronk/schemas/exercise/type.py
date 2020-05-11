from graphene_sqlalchemy import SQLAlchemyObjectType

from stronk.models.exercise import Exercise as ExerciseModel


class Exercise(SQLAlchemyObjectType):
    class Meta:
        model = ExerciseModel
