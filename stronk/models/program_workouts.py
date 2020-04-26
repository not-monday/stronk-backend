from stronk import db
from stronk.models.program import Program


class ProgramWorkouts(db.Model):
    program_id = db.Column(db.Integer,
                           db.ForeignKey('program.id'),
                           primary_key=True,
                           index=True,
                           nullable=False)
    workout_id = db.Column(db.Integer,
                           db.ForeignKey('workout.id'),
                           primary_key=True,
                           index=True,
                           nullable=False)

    def to_dict(self):
        """Returns a dictionary representing the attributes of the
        ProgramWorkouts. Key is the name of the attribute and value is the
        value of the attribute."""
        return {
            "program_id": self.get_program().to_dict(),
            "workout_id": self.get_workout().to_dict()
        }

    def get_program(self):
        """Returns Program object for the ProgramWorkouts. """
        res = Program.query.filter_by(id=self.program_id)
        if res:
            return res
        raise NoResultFound('Program does not exist.')

    def get_workout(self):
        """Returns Workout object for the ProgramWorkouts. """
        res = Workout.query.filter_by(id=self.workout_id)
        if res:
            return res
        raise NoResultFound('Workout does not exist.')

    def update(self, attrs):
        """Updates model given attrs.

        Params:
            attrs: Dictionary containing attributes to update. Key is the 
                   attribute name and value is the new value.
        """
        if attrs.get("program_id"):
            self.program_id = attrs.get("program_id")
        if attrs.get("workout_id"):
            self.workout_id = attrs.get("workout_id")
