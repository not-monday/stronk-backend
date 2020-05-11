"""Contains the Blueprint for exercises routes."""
import json

from flask import Blueprint, request, Response
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from sqlalchemy.exc import DBAPIError, IntegrityError
from werkzeug.exceptions import BadRequest, Conflict, InternalServerError, NotFound

from stronk import db
from stronk.models.exercise import Exercise

exercise_page = Blueprint('exercise', __name__)

# DELETE /exercises/:id
@exercise_page.route('/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = None
    exercise = Program.query.filter_by(id=id).first()
    if not exercise:
        raise NotFound("Exercise not found.")

    try:
        db.session.delete(exercise)
        db.session.commit()
        data = {
            "message": "Exercise successfully deleted."
        }
        body = json.dumps(data)

        return Response(body, status=200, mimetype='application/json')
    except DBAPIError as err:
        raise InternalServerError("Database Error")
