import string
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError, IntegrityError

from stronk.constants import DATABASE_ERROR_MSG
from stronk.errors.conflict import Conflict
from stronk.errors.unexpected_error import UnexpectedError

from stronk import db
from stronk.models.user import User


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    author = db.Column(db.String(),
                       index=True,
                       nullable=False)
    description = db.Column(db.String(500), nullable=False)

    @staticmethod
    def create(name, description, author):
        exercise = Exercise(name=string.capwords(name),
                            description=description,
                            author=author)
        try:
            db.session.add(exercise)
            db.session.commit()

            return exercise
        except IntegrityError as err:
            if isinstance(err.orig, UniqueViolation):
                raise Conflict("Name already used by another exercise")
            else:
                raise UnexpectedError(DATABASE_ERROR_MSG)
        except DBAPIError as err:
            raise UnexpectedError(DATABASE_ERROR_MSG)

    @staticmethod
    def find_by_id(id):
        return Exercise.query.filter_by(id=id).first()

    def to_dict(self):
        """Returns a dictionary representing the attributes of the program.
           Key is the name of the attribute and value is the value of the
           attribute. """
        return {
            "id": self.id,
            "name": self.name,
            "author": self.author,
            "description": self.description
        }

    def update(self, attrs):
        """Updates model given attrs.

        Params:
            attrs: Dictionary containing attributes to update. Key is the 
                   attribute name and value is the new value.
        """
        if attrs.get('name'):
            self.name = string.capwords(attrs.get('name'))
        if attrs.get('description'):
            self.description = attrs.get('description')
        if attrs.get('author'):
            self.author = attrs.get('author')

        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as err:
            if isinstance(err.orig, UniqueViolation):
                raise Conflict("Name already used by another exercise.")
            raise UnexpectedError(DATABASE_ERROR_MSG)
        except DBAPIError as err:
            raise UnexpectedError(DATABASE_ERROR_MSG)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except DBAPIError as err:
            raise UnexpectedError(DATABASE_ERROR_MSG)
