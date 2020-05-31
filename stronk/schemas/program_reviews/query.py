from flask import g
import graphene

from stronk.models.program_reviews import ProgramReviews as ProgramReviewsModel
from stronk.schemas.program_reviews.type import ProgramReviews


class Query(graphene.ObjectType):
    program_reviews = graphene.List(ProgramReviews)
    program_review = graphene.Field(ProgramReviews,
                                    program_id=graphene.Int(required=True))

    def resolve_program_reviews(root, info):
        """Get the program reviews made by the current user."""
        query = ProgramReviews.get_query(info)

        return query.order_by(ProgramReviewsModel.created_at.desc()).filter(
            ProgramReviewsModel.reviewer_id == g.id).all()

    def resolve_program_review(root, info, program_id: int):
        """Get a program review made by the current user."""
        query = ProgramReviews.get_query(info)

        return (query
                .filter(ProgramReviewsModel.reviewer_id == g.id,
                        ProgramReviewsModel.program_id == program_id)
                .first())
