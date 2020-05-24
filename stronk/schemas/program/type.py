import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from stronk.models.program import Program as ProgramModel
from stronk.models.program_workouts import ProgramWorkouts as ProgramWorkoutsModel
from stronk.models.user import User as UserModel
from stronk.schemas.protected_user.type import ProtectedUser
from stronk.schemas.workout.type import Workout


class Program(SQLAlchemyObjectType):
    class Meta:
        model = ProgramModel

    # Add nested querying
    author = graphene.Field(lambda: ProtectedUser)
    workouts = graphene.List(lambda: Workout)
    # TODO: Add ProgramReviews later

    def resolve_author(root, info):
        return UserModel.find_by_id(root.author)

    def resolve_workouts(root, info):
        return ProgramWorkoutsModel.find_workouts_by_program_id(root.id)
