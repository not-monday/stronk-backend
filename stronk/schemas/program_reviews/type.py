from graphene_sqlalchemy import SQLAlchemyObjectType
import graphene

from stronk.models.program_reviews import ProgramReviews as ProgramReviewsModel
from stronk.models.user import User as UserModel
from stronk.schemas.program.type import Program
from stronk.models.program import Program as ProgramModel
from stronk.schemas.protected_user.type import ProtectedUser


class ProgramReviews(SQLAlchemyObjectType):
    class Meta:
        model = ProgramReviewsModel
        exclude_fields = ('reviewer_id', 'program_id')

    reviewer = graphene.Field(ProtectedUser)
    program = graphene.Field(Program)

    def resolve_reviewer(root, info):
        return UserModel.find_by_id(root.reviewer_id)

    def resolve_program(root, info):
        return ProgramModel.find_by_id(root.program_id)
