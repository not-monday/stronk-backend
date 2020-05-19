from flask import current_app
from stronk import db
from sqlalchemy.exc import DBAPIError
from werkzeug.exceptions import InternalServerError, Conflict

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    projected_time = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        """Returns a dictionary representing the attributes of the program.
           Key is the name of the attribute and value is the value of the
           attribute. """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "projected_time": self.projected_time
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

        
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            data = {
                "message": "Workout successfully deleted."
            }
        except DBAPIError as err:
            raise InternalServerError("Database Error")
    
    @staticmethod
    def create(name, description, projected_time):
        workout = Workout(
            name=name,
            description=description if description else "",
            projected_time = projected_time if projected_time else 0
            )

        try:
            db.session.add(workout)
            db.session.commit()

            return workout
        except DBAPIError as err:
            raise InternalServerError("Database Error")


    @staticmethod
    def find_by_id(id):
        return Workout.query.filter_by(id=id).first()
