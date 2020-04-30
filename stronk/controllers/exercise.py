"""Contains the Blueprint for exercises routes."""
import json

from flask import Blueprint, request, Response
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from sqlalchemy.exc import DBAPIError, IntegrityError
from werkzeug.exceptions import BadRequest, Conflict, InternalServerError, NotFound

from stronk import db
from stronk.models.exercise import Exercise

exercise_page = Blueprint('exercise', __name__)

# GET /exercises
@exercise_page.route('/', methods=['GET'])
def get_exercises():
    try:
        exercises = Exercise.query.all()
    except DBAPIError:
        raise InternalServerError("Database Error")

    data = []
    for exercise in exercises:
        data.append(exercise.to_dict())

    body = json.dumps(data)
    res = Response(body, status=200, mimetype='application/json')

    return res

# GET /exercises/:id
@exercise_page.route('/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.filter_by(id=id).first()
    if not exercise:
        raise NotFound("Exercise not found.")

    body = json.dumps(exercise.to_dict())
    res = Response(body, status=200, mimetype='application/json')

    return res

# POST /exercises
@exercise_page.route('/', methods=['POST'])
def add_exercise():
    req_body = request.get_json()

    # TODO: Move to custom create function that includes validation
    if not req_body.get('name'):
        raise BadRequest("Missing name attribute creating exercise.")

    if not req_body.get('description'):
        raise BadRequest("Missing description attribute creating exercise.")

    e = Exercise(author=req_body['name'], name=req_body['description'])

    try:
        db.session.add(e)
        db.session.commit()
        body = json.dumps(e.to_dict())
        res = Response(body, status=200, mimetype='application/json')

        return res
    except DBAPIError as err:
        raise InternalServerError("Database Error")

# PATCH /exercise/:id
@exercise_page.route('/<int:id>', methods=['PATCH'])
def update_exercise(id):
    exercise = Exercise.query.filter_by(id=id).first()
    if not exercise:
        raise NotFound("Exercise not found.")

    req_body = request.get_json()
    exercise.update(req_body)

    try:
        db.session.commit()
        body = json.dumps(exercise.to_dict())
        return Response(body,
                        status=200,
                        mimetype='application/json')
    except IntegrityError as err:
        if isinstance(err.orig, UniqueViolation):
            return Conflict("Exercise with ID already exists.")
    except DBAPIError as err:
        raise InternalServerError("Database Error")

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
