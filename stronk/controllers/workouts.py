"""Contains the Blueprint for workouts routes."""
import json
from flask import Blueprint, request, Response
from sqlalchemy.exc import DBAPIError, IntegrityError
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from stronk.models.workout import Workout
from stronk.errors import api_errors as e
from stronk import db

workouts_page = Blueprint('workout', __name__)

# GET /workouts
@workouts_page.route('/', methods=['GET'])
def get_workouts():
    try:
        workouts = Workout.query.all()
    except DBAPIError:
        return e.internal_server_error()

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
        return e.not_found_error()
    
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
        return e.bad_request()

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
        if isinstance(err.orig, ForeignKeyViolation):
            return e.bad_request()
        elif isinstance(err.orig, UniqueViolation):
            return e.conflict()
    except DBAPIError as err:
        return e.internal_server_error()

# PATCH /workout/:id
@workouts_page.route('/<int:id>', methods=['PATCH'])
def update_workout(id):
    workout = Workout.query.filter_by(id=id).first()
    if not workout:
        return e.not_found_error()

    req_body = request.get_json()
    workout.update(req_body)

    try:
        db.session.commit()
        body = json.dumps(workout.to_dict())
        return Response(body,
                        status=200,
                        mimetype='application/json')
    except IntegrityError as err:
        if isinstance(err.orig, ForeignKeyViolation):
            return e.bad_request()
        elif isinstance(err.orig, UniqueViolation):
            return e.conflict()
    except DBAPIError as err:
        return e.internal_server_error()

# DELETE /workouts/:id
@workouts_page.route('/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = None
    workout = Program.query.filter_by(id=id).first()
    if not workout:
        return e.not_found_error()

    try:
        db.session.delete(workout)
        db.session.commit()
        data = {
            "message": "Workout successfully deleted."
        }
        body = json.dumps(data)

        return Response(body, status=200, mimetype='application/json')
    except DBAPIError as err:
        return e.internal_server_error()    
