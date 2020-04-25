from sqlalchemy import CheckConstraint
from stronk import db
from stronk.models.program import Program
from stronk.models.user import User


class ProgramReviews(db.Model):
    __table_args__ = (CheckConstraint('rating <= 5'),)
    program_id = db.Column(db.Integer,
                           db.ForeignKey('program.id'),
                           primary_key=True,
                           index=True,
                           nullable=False)
    reviewer_id = db.Column(db.Integer,
                            db.ForeignKey('user.id'),
                            primary_key=True,
                            index=True,
                            nullable=False)
    rating = db.Column(db.Integer,
                       nullable=False)
    comments = db.Column(db.String(250), nullable=False)

    @classmethod
    def get_reviews_by_program_id(cls, program_id):
        """Returns a list of all reviews for a program with id."""
        return {
            "program": self.get_program(program_id=program_id).to_dict(),
            "reviews": cls.query.filter_by(program_id=program_id)
        }

    def to_dict(self):
        """Returns a dictionary representing the attributes of the
           ProgramReviews. Key is the name of the attribute and value is the
           value of the attribute."""
        return {
            "program": self.get_program().to_dict(),
            "reviewer": self.get_user().to_dict(),
            "rating": self.rating,
            "comments": self.comments
        }

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
