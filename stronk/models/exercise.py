import string
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError, IntegrityError
from werkzeug.exceptions import BadRequest, Conflict, InternalServerError

from stronk import db


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False, unique=True)
    description = db.Column(db.String(500), nullable=False)

    @staticmethod
    def create(name, description):
        exercise = Exercise(name=string.capwords(name),
                            description=description)

        try:
            db.session.add(exercise)
            db.session.commit()

            return exercise
        except IntegrityError as err:
            if isinstance(err.orig, UniqueViolation):
                raise BadRequest("Name already used by another exercise")
            else:
                raise InternalServerError("Database Error")
        except DBAPIError as err:
            raise InternalServerError("Database Error")

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
            "description": self.description,
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

        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as err:
            if isinstance(err.orig, UniqueViolation):
                raise Conflict("Name already used by another exercise.")
            raise InternalServerError("Database Error")
        except DBAPIError as err:
            raise InternalServerError("Database Error")

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            data = {
                "message": "Exercise successfully deleted."
            }
        except DBAPIError as err:
            raise InternalServerError("Database Error")
