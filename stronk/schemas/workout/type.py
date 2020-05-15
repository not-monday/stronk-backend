from graphene_sqlalchemy import SQLAlchemyObjectType

from stronk.models.workout import Workout as WorkoutModel

class Workout(SQLAlchemyObjectType):
    class Meta: 
        model = WorkoutModel