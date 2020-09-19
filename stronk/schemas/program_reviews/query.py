from flask import g
import graphene

from stronk.constants import PROGRAM_NOT_FOUND_MSG, USER_NOT_FOUND_MSG
from stronk.errors.bad_request import BadRequest
from stronk.models.program import Program as ProgramModel
from stronk.models.program_reviews import ProgramReviews as ProgramReviewsModel
from stronk.models.user import User as UserModel
from stronk.schemas.program_reviews.type import ProgramReviews

class Query(graphene.ObjectType):
    program_reviews = graphene.List(ProgramReviews,
                                    program_id=graphene.Int(),
                                    username=graphene.String())
    program_review = graphene.Field(ProgramReviews,
                                    program_id=graphene.Int(required=True),
                                    username=graphene.String(required=True))

    def resolve_program_reviews(root,
                                info,
                                program_id: int = None,
                                username: str = None):
        """Get the program reviews by program or by user."""
        query = ProgramReviews.get_query(info)
        if not (program_id or username):
            raise BadRequest("Either program_id or username must be given.")
        if username:
            user = UserModel.find_by_username(username)
            if not user:
                raise NotFound(USER_NOT_FOUND_MSG)
            return query.order_by(ProgramReviewsModel.created_at.desc()).filter(
                ProgramReviewsModel.reviewer_id == user.id).all()
            )
        else:
            program = ProgramModel.find_by_id(program_id)
            if not program:
                raise NotFound(PROGRAM_NOT_FOUND_MSG)
            return query.order_by(ProgramReviewsModel.created_at.desc()).filter(
                ProgramReviewsModel.program_id == program_id).all()

    def resolve_program_review(root, info, program_id: int, username: str):
        """Get a program review made by a user for a program.
        
        program_id: The parent_id of the program.
        username: User's username.
        """
        query = ProgramReviews.get_query(info)
        user = UserModel.find_by_username(username)
        if not user:
            raise NotFound(USER_NOT_FOUND_MSG)
        program = ProgramModel.find_by_id(program_id)
        if not program:
            raise NotFound(PROGRAM_NOT_FOUND_MSG)
        return (query
                .filter(ProgramReviewsModel.reviewer_id == user.id,
                        ProgramReviewsModel.program_id == program_id)
                .first())
