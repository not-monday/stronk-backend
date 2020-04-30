"""Contains the Blueprint for programs routes."""
import json

from flask import Blueprint, request, Response
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from sqlalchemy.exc import DBAPIError, IntegrityError
from werkzeug.exceptions import BadRequest, Conflict, InternalServerError, NotFound

from stronk import db
from stronk.models.program import Program

programs_page = Blueprint('program', __name__)

# GET /programs
@programs_page.route('/', methods=['GET'])
def get_programs():
    try:
        programs = Program.query.all()
    except DBAPIError:
        raise InternalServerError("Database Error")

    data = []
    for program in programs:
        data.append(program.to_dict())

    body = json.dumps(data)
    res = Response(body, status=200, mimetype='application/json')

    return res

# GET /programs/:id
@programs_page.route('/<int:id>', methods=['GET'])
def get_program(id):
    program = Program.query.filter_by(id=id).first()
    if not program:
        raise NotFound("Program not found.")

    body = json.dumps(program.to_dict())
    res = Response(body, status=200, mimetype='application/json')

    return res

# POST /programs
@programs_page.route('/', methods=['POST'])
def add_program():
    req_body = request.get_json()
    # TODO: Move to custom create function that includes validation
    if not (req_body.get('author')
            and req_body.get('name')
            and req_body.get('duration')
            and req_body.get('description')):
        raise BadRequest(
            "Attributes author, name, duration, description are required.")

    p = Program(author=req_body['author'],
                name=req_body['name'],
                duration=req_body['duration'],
                description=req_body['description'])

    try:
        db.session.add(p)
        db.session.commit()
        body = json.dumps(p.to_dict())
        res = Response(body, status=200, mimetype='application/json')

        return res
    except IntegrityError as err:
        if isinstance(err.orig, ForeignKeyViolation):
            raise BadRequest("Author does not exist.")
        elif isinstance(err.orig, UniqueViolation):
            raise Conflict("Program with ID already exists.")
    except DBAPIError as err:
        raise InternalServerError("Database Error")

# PATCH /program/:id
@programs_page.route('/<int:id>', methods=['PATCH'])
def update_program(id):
    program = Program.query.filter_by(id=id).first()
    if not program:
        raise NotFound("Program not found.")

    req_body = request.get_json()
    program.update(req_body)

    try:
        db.session.commit()
        body = json.dumps(program.to_dict())
        return Response(body,
                        status=200,
                        mimetype='application/json')
    except IntegrityError as err:
        if isinstance(err.orig, ForeignKeyViolation):
            raise BadRequest("Author does not exist.")
        elif isinstance(err.orig, UniqueViolation):
            raise Conflict("Program with ID already exists.")
    except DBAPIError as err:
        raise InternalServerError("Database Error")

# DELETE /programs/:id
@programs_page.route('/<int:id>', methods=['DELETE'])
def delete_program(id):
    program = None
    program = Program.query.filter_by(id=id).first()
    if not program:
        raise NotFound("Program not found.")

    try:
        db.session.delete(program)
        db.session.commit()
        data = {
            "message": "Program successfully deleted."
        }
        body = json.dumps(data)

        return Response(body, status=200, mimetype='application/json')
    except DBAPIError as err:
        raise InternalServerError("Database Error")
