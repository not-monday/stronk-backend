import graphene
from flask import g

from stronk.errors.bad_attributes import BadAttributes
from stronk.errors.not_found import NotFound
from stronk.models.program import Program as ProgramModel
from stronk.models.program_reviews import ProgramReviews as ProgramReviewsModel
from stronk.schemas.program_reviews.type import ProgramReviews


class CreateProgramReview(graphene.Mutation):
    """Create a review for a program"""
    program_review = graphene.Field(ProgramReviews)

    class Arguments:
        program_id = graphene.Int(required=True)
        rating = graphene.Int(required=True)
        comments = graphene.String(required=True)

    def mutate(root, info, program_id: int, rating: int, comments: str):
        if rating > 5 or rating < 0:
            raise BadAttributes("rating must be between 1 and 5 inclusive.")
        ProgramModel.find_by_id(program_id)
        program_review = ProgramReviewsModel.create(reviewer_id=g.id,
                                                    program_id=program_id,
                                                    rating=rating,
                                                    comments=comments)

        return CreateProgramReview(program_review=program_review)


class DeleteProgramReview(graphene.Mutation):
    """Delete a review for a program. Throws a NotFound error review is not
    found."""
    ok = graphene.Boolean()

    class Arguments:
        program_id = graphene.Int(required=True)

    def mutate(root, info, program_id: int):
        review = (ProgramReviewsModel
                  .get_by_reviewer_and_program_id(g.id, program_id))
        if not review:
            raise NotFound("Review not found.")
        review.delete()
        ok = True

        return DeleteProgramReview(ok=ok)


class Mutation(graphene.ObjectType):
    create_program_review = CreateProgramReview.Field()
    delete_program_review = DeleteProgramReview.Field()
