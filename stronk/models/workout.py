from datetime import datetime
from flask import current_app
from sqlalchemy.exc import DBAPIError

from stronk import db
from stronk.constants import DATABASE_ERROR_MSG, INVALID_WORKOUT_START_TIME
from stronk.errors.conflict import Conflict
from stronk.errors.bad_attributes import BadAttributes
from stronk.errors.unexpected_error import UnexpectedError


class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    projected_time = db.Column(db.Integer, nullable=False)
    scheduled_time = db.Column(db.DateTime(timezone=True), nullable=True)

    def to_dict(self):
        """Returns a dictionary representing the attributes of the program.
           Key is the name of the attribute and value is the value of the
           attribute. """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "projected_time": self.projected_time,
            "scheduled_time": self.scheduled_time
        }

    def update(self, attrs):
        """Updates model given attrs.

        Params:
            attrs: Dictionary containing attributes to update. Key is the 
                   attribute name and value is the new value.
        """
        if attrs.get('name'):
            self.name = attrs.get('name')
        if attrs.get('description'):
            self.description = attrs.get('description')
        if attrs.get('projected_time'):
            self.projected_time = attrs.get('projected_time')
        if attrs.get("scheduled_time"):
            ensure_valid_time(scheduled_time)
            self.scheduled_time = attrs.get("scheduled_time")

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except DBAPIError as err:
            raise UnexpectedError(DATABASE_ERROR_MSG)

    @staticmethod
    def create(name, description, projected_time, scheduled_time: datetime):
        ensure_valid_time(scheduled_time)

        workout = Workout(
            name=name,
            description=description if description else "",
            projected_time=projected_time if projected_time else 0,
            scheduled_time=scheduled_time
        )

        try:
            db.session.add(workout)
            db.session.commit()

            return workout
        except DBAPIError as err:
            raise UnexpectedError(DATABASE_ERROR_MSG)

    def ensure_valid_time(scheduled_time: datetime):
        # fail if the scheduled time is not in the future
        if (scheduled_time and scheduled_time < datetime.now(scheduled_time.tzinfo)):
            raise BadAttributes(INVALID_WORKOUT_START_TIME)

    @staticmethod
    def find_by_id(id):
        return Workout.query.filter_by(id=id).first()

    def clone(self):
        return Workout.create(
            name=self.name, 
            description=self.description, 
            projected_time=self.projected_time, 
            scheduled_time=self.scheduled_time
        )
