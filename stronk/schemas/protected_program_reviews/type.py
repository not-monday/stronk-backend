from graphene_sqlalchemy import SQLAlchemyObjectType
import graphene

from stronk.models.program_reviews import ProgramReviews as ProgramReviewsModel
from stronk.models.user import User as UserModel
from stronk.schemas.protected_user.type import ProtectedUser


class ProtectedProgramReviews(SQLAlchemyObjectType):
    class Meta:
        model = ProgramReviewsModel
        exclude_fields = ('reviewer_id', )

    reviewer = graphene.Field(ProtectedUser)

    def resolve_reviewer(root, info):
        return UserModel.find_by_id(root.reviewer_id)
