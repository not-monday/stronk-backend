from datetime import timedelta
from psycopg2.errors import ForeignKeyViolation
from sqlalchemy.exc import DBAPIError, IntegrityError

from stronk import db
from stronk.constants import DATABASE_ERROR_MSG, USER_NOT_FOUND_MSG
from stronk.errors.bad_attributes import BadAttributes
from stronk.errors.unexpected_error import UnexpectedError
from stronk.models.user import User
from stronk.utils.date import date_str_to_date


class Weight(db.Model):
    user_id = db.Column(db.String(),
                        db.ForeignKey(f'{User.__tablename__}.id'),
                        primary_key=True,
                        index=True,
                        nullable=False)
    weight = db.Column(db.Float, nullable=False)
    measured_at = db.Column(db.DateTime(timezone=True),
                            primary_key=True, nullable=False)

    @staticmethod
    def create(user_id, weight, measured_at):
        """Insert a weight for a user."""

        weight = Weight(user_id=user_id, weight=weight,
                        measured_at=measured_at)

        try:
            db.session.add(weight)
            db.session.commit()

            return weight
        except IntegrityError as err:
            if isinstance(err.orig, ForeignKeyViolation):
                raise BadAttributes(USER_NOT_FOUND_MSG)
            else:
                raise UnexpectedError(DATABASE_ERROR_MSG)
        except DBAPIError as err:
            raise UnexpectedError(DATABASE_ERROR_MSG)

    @staticmethod
    def get_weights_by_user_id(user_id, limit=None):
        """Returns a list of all weights for a user sorted by decreasing
           measuredAt."""
        q = (Weight
             .query
             .order_by(Weight.measured_at.desc())
             .filter_by(user_id=user_id))

        if limit:
            return q.limit(limit).all()

        return q.all()

    @staticmethod
    def get_weight_by_date(user_id, measured_at):
        """Returns the weight of a user measured on a date. Date should be in
        UTC.
        """
        start_date = date_str_to_date(measured_at)
        end_date = start_date + timedelta(days=1)
        return (Weight
                .query
                .filter(Weight.measured_at >= str(start_date),
                        Weight.measured_at < str(end_date),
                        Weight.user_id == user_id)
                .first())

    def get_user(self, user_id=None):
        """Returns User object for the Weight. """
        u_id = user_id if user_id else self.user_id
        res = User.query.filter_by(id=u_id)
        if res:
            return res
        raise NoResultFound('User does not exist.')

    def update(self, attrs):
        """Updates model given attrs.

        Params:
            attrs: Dictionary containing attributes to update. Key is the 
                   attribute name and value is the new value.
        """
        if attrs.get('weight'):
            self.weight = attrs.get('weight')

        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as err:
            if isinstance(err.orig, ForeignKeyViolation):
                raise BadAttributes(USER_NOT_FOUND_MSG)
            else:
                raise UnexpectedError(DATABASE_ERROR_MSG)
        except DBAPIError as err:
            raise UnexpectedError(DATABASE_ERROR_MSG)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except DBAPIError as err:
            raise UnexpectedError(DATABASE_ERROR_MSG)
