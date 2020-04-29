"""Contains the Blueprint for workouts routes."""
import json

from flask import Blueprint, request, Response
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from sqlalchemy.exc import DBAPIError, IntegrityError
from werkzeug.exceptions import BadRequest, Conflict, InternalServerError, NotFound

from stronk import db
from stronk.models.workout import Workout

workouts_page = Blueprint('workout', __name__)

# GET /workouts
@workouts_page.route('/', methods=['GET'])
def get_workouts():
    try:
        workouts = Workout.query.all()
    except DBAPIError:
        raise InternalServerError("Databse Error")

    data = []
    for workout in workouts:
        data.append(workout.to_dict())

    body = json.dumps(data)
    res = Response(body, status=200, mimetype='application/json')

    return res

# GET /workouts/:id
@workouts_page.route('/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.filter_by(id=id).first()
    if not workout:
        raise NotFound("Workouts not found.")

    body = json.dumps(workout.to_dict())
    res = Response(body, status=200, mimetype='application/json')

    return res

# POST /workouts
@workouts_page.route('/', methods=['POST'])
def add_workout():
    req_body = request.get_json()

    # TODO: Move to custom create function that includes validation
    if not (req_body.get('name')
            and req_body.get('description')
            and req_body.get('projected_time')):
        raise BadRequest(
            "Attributes name, description, projected_time are required.")

    w = Workout(author=req_body['name'],
                name=req_body['description'],
                duration=req_body['projected_time'])

    try:
        db.session.add(w)
        db.session.commit()
        body = json.dumps(w.to_dict())
        res = Response(body, status=200, mimetype='application/json')

        return res
    except IntegrityError as err:
        if isinstance(err.orig, UniqueViolation):
            raise Conflict("Workout with ID already exists.")
    except DBAPIError as err:
        raise InternalServerError("Databse Error")

# PATCH /workout/:id
@workouts_page.route('/<int:id>', methods=['PATCH'])
def update_workout(id):
    workout = Workout.query.filter_by(id=id).first()
    if not workout:
        raise NotFound("Workouts not found.")

    req_body = request.get_json()
    workout.update(req_body)

    try:
        db.session.commit()
        body = json.dumps(workout.to_dict())
        return Response(body,
                        status=200,
                        mimetype='application/json')
    except IntegrityError as err:
        if isinstance(err.orig, UniqueViolation):
            raise Conflict("Workout with ID already exists.")
    except DBAPIError as err:
        raise InternalServerError("Databse Error")

# DELETE /workouts/:id
@workouts_page.route('/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = None
    workout = Program.query.filter_by(id=id).first()
    if not workout:
        raise NotFound("Workouts not found.")

    try:
        db.session.delete(workout)
        db.session.commit()
        data = {
            "message": "Workout successfully deleted."
        }
        body = json.dumps(data)

        return Response(body, status=200, mimetype='application/json')
    except DBAPIError as err:
        raise InternalServerError("Databse Error")
