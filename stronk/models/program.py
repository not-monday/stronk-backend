import string
from psycopg2.errors import ForeignKeyViolation, UniqueViolation
from sqlalchemy.exc import DBAPIError, IntegrityError

from stronk.constants import DATABASE_ERROR_MSG, USER_NOT_FOUND_MSG
from stronk import db
from stronk.errors.bad_attributes import BadAttributes
from stronk.errors.conflict import Conflict
from stronk.errors.unexpected_error import UnexpectedError
from stronk.models.user import User


class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(),
                       db.ForeignKey(f'{User.__tablename__}.id'),
                       index=True,
                       nullable=False)
    name = db.Column(db.String(128), index=True, nullable=False, unique=True)
    duration = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(256), nullable=False)

    @staticmethod
    def create(author, name, duration, description):
        program = Program(author=author,
                          name=string.capwords(name),
                          duration=duration,
                          description=description)

        try:
            db.session.add(program)
            db.session.commit()

            return program
        except IntegrityError as err:
            if isinstance(err.orig, UniqueViolation):
                raise Conflict("Name already used by another program")
            elif isinstance(err.orig, ForeignKeyViolation):
                raise BadAttributes(USER_NOT_FOUND_MSG)
            else:
                raise UnexpectedError(DATABASE_ERROR_MSG)
        except DBAPIError as err:
            raise UnexpectedError(DATABASE_ERROR_MSG)

    @staticmethod
    def find_by_id(id):
        return Program.query.filter_by(id=id).first()

    def to_dict(self):
        """Returns a dictionary representing the attributes of the program.
           Key is the name of the attribute and value is the value of the
           attribute. """
        return {
            "id": self.id,
            "author": self.get_author(),
            "name": self.name,
            "duration": self.duration,
            "description": self.description
        }

    def get_author(self):
        """Returns the User object for the author of the program."""
        return User.query.filter_by(id=self.author).first().to_dict()

    def update(self, attrs):
        """Updates model given attrs.

        Params:
            attrs: Dictionary containing attributes to update. Key is the 
                   attribute name and value is the new value.
        """
        if attrs.get('author'):
            self.author = attrs.get('author')
        if attrs.get('name'):
            self.name = string.capwords(attrs.get('name'))
        if attrs.get('duration'):
            self.duration = attrs.get('duration')
        if attrs.get('description'):
            self.description = attrs.get('description')

        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as err:
            if isinstance(err.orig, ForeignKeyViolation):
                raise BadAttributes("Author does not exist.")
            elif isinstance(err.orig, UniqueViolation):
                raise Conflict("Program with name already exists.")
        except DBAPIError as err:
            raise UnexpectedError(DATABASE_ERROR_MSG)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            data = {
                "message": "Program successfully deleted."
            }
        except DBAPIError as err:
            raise UnexpectedError(DATABASE_ERROR_MSG)
