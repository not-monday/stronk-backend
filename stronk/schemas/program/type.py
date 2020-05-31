import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from stronk.models.program import Program as ProgramModel
from stronk.models.program_reviews import ProgramReviews as ProgramReviewsModel
from stronk.models.program_workouts import ProgramWorkouts as ProgramWorkoutsModel
from stronk.models.user import User as UserModel
from stronk.schemas.protected_program_reviews.type import ProtectedProgramReviews
from stronk.schemas.protected_user.type import ProtectedUser
from stronk.schemas.workout.type import Workout


class Program(SQLAlchemyObjectType):
    class Meta:
        model = ProgramModel

    # Add nested querying
    author = graphene.Field(ProtectedUser)
    workouts = graphene.List(Workout)
    program_reviews = graphene.List(ProtectedProgramReviews)

    def resolve_author(root, info):
        return UserModel.find_by_id(root.author)

    def resolve_workouts(root, info):
        return ProgramWorkoutsModel.find_workouts_by_program_id(root.id)

    def resolve_program_reviews(root, info):
        return ProgramReviewsModel.get_reviews_by_program_id(root.id)
