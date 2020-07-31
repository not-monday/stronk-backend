import datetime

from sqlalchemy import CheckConstraint
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from sqlalchemy.exc import DBAPIError, IntegrityError

from stronk import db
from stronk.constants import DATABASE_ERROR_MSG, PROGRAM_NOT_FOUND_MSG
from stronk.errors.bad_attributes import BadAttributes
from stronk.errors.conflict import Conflict
from stronk.errors.unexpected_error import UnexpectedError
from stronk.models.program import Program
from stronk.models.user import User


class ProgramReviews(db.Model):
    __table_args__ = (CheckConstraint('rating <= 5 AND rating > 0'),)
    program_id = db.Column(db.Integer,
                           db.ForeignKey('program.id'),
                           primary_key=True,
                           index=True,
                           nullable=False)
    reviewer_id = db.Column(db.String(),
                            db.ForeignKey(f'{User.__tablename__}.id'),
                            primary_key=True,
                            index=True,
                            nullable=False)
    rating = db.Column(db.Integer,
                       nullable=False)
    comments = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    @staticmethod
    def create(reviewer_id, program_id, rating, comments):
        now = datetime.datetime.now()
        program_review = ProgramReviews(reviewer_id=reviewer_id,
                                        program_id=program_id,
                                        rating=rating,
                                        comments=comments,
                                        created_at=now)

        try:
            db.session.add(program_review)
            db.session.commit()

            return program_review
        except IntegrityError as err:
            if isinstance(err.orig, UniqueViolation):
                raise Conflict("User already reviewed this program")
            elif isinstance(err.orig, ForeignKeyViolation):
                raise BadAttributes("User or Program not found.")
            else:
                raise UnexpectedError(DATABASE_ERROR_MSG)
        except DBAPIError as err:
            raise UnexpectedError(DATABASE_ERROR_MSG)

    @staticmethod
    def get_reviews_by_program_id(program_id):
        """Returns a list of all reviews for a program with id."""
        return (ProgramReviews
                .query
                .order_by(ProgramReviews.created_at.desc())
                .filter_by(program_id=program_id)
                .all())

    @staticmethod
    def get_reviews_by_reviewer_id(reviewer_id):
        """Returns a list of all reviews by a user."""
        return (ProgramReviews
                .query
                .order_by(ProgramReviews.created_at.desc())
                .filter_by(reviewer_id=reviewer_id)
                .all())

    @staticmethod
    def get_by_reviewer_and_program_id(reviewer_id: str, program_id: int):
        """Returns a program review based on the reviewer id and program id."""
        return (ProgramReviews.query.filter_by(reviewer_id=reviewer_id,
                                               program_id=program_id).first())

    def get_program(self, program_id=None):
        """Returns Program object for the ProgramReviews. """
        p_id = program_id if program_id else self.program_id
        res = Program.query.filter_by(id=p_id)
        if res:
            return res
        raise NoResultFound('Program does not exist.')

    def get_user(self):
        """Returns User object for the ProgramReviews. """
        res = User.query.filter_by(id=self.reviewer_id)
        if res:
            return res
        raise NoResultFound('Program does not exist.')

    def update(self, attrs):
        """Updates model given attrs.

        Params:
            attrs: Dictionary containing attributes to update. Key is the 
                   attribute name and value is the new value.
        """
        if attrs.get("program_id"):
            self.program_id = attrs.get("program_id")
        if attrs.get("reviewer_id"):
            self.reviewer_id = attrs.get("reviewer_id")

    def delete(self):
        """Delete program review."""
        try:
            db.session.delete(self)
            db.session.commit()
        except DBAPIError as err:
            raise UnexpectedError(DATABASE_ERROR_MSG)
