from graphene_sqlalchemy import SQLAlchemyObjectType

from stronk.models.program_workouts import ProgramWorkouts as ProgramWorkoutModel
from stronk.models.workout import Workout as WorkoutModel
class Workout(SQLAlchemyObjectType):
    class Meta: 
        model = WorkoutModel


# the `SQLAlchemyObjectType` rep of relations that serve to connect a two models should always be located
# in the file for the foreign relation (since they are used only for it)
class ProgramWorkouts(SQLAlchemyObjectType):
    class Meta:
        model = ProgramWorkoutModel