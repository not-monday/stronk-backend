"""Contains the Blueprint for programs routes."""
import json
from flask import Blueprint, request, Response
from sqlalchemy.exc import DBAPIError, IntegrityError
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from stronk.models.program import Program
from stronk.errors import api_errors as e
from stronk import db

programs_page = Blueprint('program', __name__)

# GET /programs
@programs_page.route('/', methods=['GET'])
def get_programs():
    try:
        programs = Program.query.all()
    except DBAPIError:
        return e.internal_server_error()

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
        return e.not_found_error()
    
    body = json.dumps(program.to_dict())
    res = Response(body, status=200, mimetype='application/json')
    
    return res

# POST /programs
@programs_page.route('/', methods=['POST'])
def add_program():
    req_body = request.get_json()
    
    if not (req_body.get('author')
            and req_body.get('name')
            and req_body.get('duration')
            and req_body.get('description')):
        return e.bad_request()

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
            return e.bad_request()
        elif isinstance(err.orig, UniqueViolation):
            return e.conflict()
    except DBAPIError as err:
        return e.internal_server_error()

# PATCH /program/:id
# TODO move logic for updating to Program model
@programs_page.route('/<int:id>', methods=['PATCH'])
def update_program(id):
    program = Program.query.filter_by(id=id).first()
    if not program:
        return e.not_found_error()

    req_body = request.get_json()

    if req_body.get('author'):
        program.author = req_body.get('author')
    if req_body.get('name'):
        program.name = req_body.get('name')
    if req_body.get('duration'):
        program.duration = req_body.get('duration')
    if req_body.get('description'):
        program.description = req_body.get('description')
    
    try:
        db.session.commit()

        return Response(program.to_dict(), status=200, mimetype='application/json')
    except IntegrityError as err:
        if isinstance(err.orig, ForeignKeyViolation):
            return e.bad_request()
        elif isinstance(err.orig, UniqueViolation):
            return e.conflict()
    except DBAPIError as err:
        return e.internal_server_error()


# DELETE /programs/:id
# TODO fix
@programs_page.route('/<int:id>', methods=['DELETE'])
def delete_program(id):
    program = None
    program = Program.query.filter_by(id=id).first()
    if not program:
        return e.not_found_error()

    try:
        db.session.delete(program)
        db.session.commit()
        data = {
            "message": "Program successfully deleted."
        }
        body = json.dumps(data)

        return Response(body, status=200, mimetype='application/json')
    except DBAPIError as err:
        return e.internal_server_error()    
