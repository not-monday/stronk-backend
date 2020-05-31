from stronk import db
from stronk.constants import DATABASE_ERROR_MSG
from stronk.errors.unexpected_error import UnexpectedError
from stronk.errors.conflict import Conflict
from stronk.models.program import Program
from stronk.models.workout import Workout

from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import DBAPIError, IntegrityError


class ProgramWorkouts(db.Model):
    program_id = db.Column(db.Integer,
                           db.ForeignKey('program.id'),
                           index=True,
                           nullable=False)
    workout_id = db.Column(db.Integer,
                           db.ForeignKey('workout.id'),
                           primary_key=True,
                           index=True,
                           nullable=False)

    @staticmethod
    def create(program_id, workout_id):
        program_workout = ProgramWorkouts(
            program_id=program_id, workout_id=workout_id)

        try:
            db.session.add(program_workout)
            db.session.commit()

            return program_workout
        except IntegrityError as err:
            if isinstance(err.orig, UniqueViolation):
                raise Conflict("Program workout already exists")
            else:
                raise UnexpectedError(DATABASE_ERROR_MSG)
        except DBAPIError as err:
            print("* err")
            print(err)
            raise UnexpectedError(DATABASE_ERROR_MSG)

    @staticmethod
    def find_by_workout_id(workout_id):
        return ProgramWorkouts.query.filter_by(workout_id=workout_id).first()

    @staticmethod
    def filter_by_program_id(program_id):
        """Returns all rows with program_id."""
        return ProgramWorkouts.query.filter_by(program_id=program_id).all()

    @staticmethod
    def find_workouts_by_program_id(program_id: int):
        """Returns list of Workouts that belong to a program with program_id."""
        rows = ProgramWorkouts.filter_by_program_id(program_id)
        ids = []
        for row in rows:
            ids.append(row.workout_id)
        return db.session.query(Workout).filter(Workout.id.in_(ids)).order_by(Workout.name).all()

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

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except DBAPIError as err:
            raise UnexpectedError(DATABASE_ERROR_MSG)
