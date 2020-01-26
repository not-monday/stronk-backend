"""Contains the Blueprint for users routes."""
import json
from flask import Blueprint, request, Response
from sqlalchemy.exc import DBAPIError, IntegrityError
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from stronk.models.user import User
from stronk.errors import api_errors as e
from stronk import db

users_page = Blueprint('users', __name__)

# GET /users
@users_page.route('/', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
    except DBAPIError:
        return e.internal_server_error()

    data = []
    for user in users:
        data.append(user.to_dict())
    
    body = json.dumps(data)
    res = Response(body, status=200, mimetype='application/json')

    return res

# GET /users/:id
@users_page.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return e.not_found_error()
    
    body = json.dumps(user.to_dict())
    res = Response(body, status=200, mimetype='application/json')

    return res

# POST /users
@users_page.route('/', methods=['POST'])
def add_user():
    req_body = request.get_json()
    
    if not (req_body.get('name')
            and req_body.get('username')
            and req_body.get('email')
            and req_body.get('password_hash')):
        return e.bad_request()

    u = User(name=req_body['name'],
            username=req_body['username'],
            email=req_body['email'],
            password_hash=req_body['password_hash'])
    if req_body.get('current_program'):
        u.current_program = req_body['current_program']
    
    try:
        db.session.add(u)
        db.session.commit()
        body = json.dumps(u.to_dict())
        res = Response(body, status=200, mimetype='application/json')

        return res
    except IntegrityError as err:
        if isinstance(err.orig, ForeignKeyViolation):
            return e.bad_request()
        elif isinstance(err.orig, UniqueViolation):
            return e.conflict()
    except DBAPIError as err:
        return e.internal_server_error()

# PATCH /users/:id
# TODO move logic for updating to User model
@users_page.route('/<int:id>', methods=['PATCH'])
def update_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        return e.not_found_error()

    req_body = request.get_json()

    if req_body.get('name'):
        user.name = req_body.get('name')
    if req_body.get('email'):
        user.email = req_body.get('email')
    if req_body.get('username'):
        user.username = req_body.get('username')
    if req_body.get('password_hash'):
        user.password_hash = req_body.get('password_hash')
    if req_body.get('current_program'):
        user.current_program = req_body.get('current_program')
    
    try:
        db.session.commit()

        return Response(user.to_dict(), status=200, mimetype='application/json')
    except IntegrityError as err:
        if isinstance(err.orig, ForeignKeyViolation):
            return e.bad_request()
        elif isinstance(err.orig, UniqueViolation):
            return e.conflict()
    except DBAPIError as err:
        return e.internal_server_error()

# DELETE /users/:id
# TODO fix
@users_page.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = None
    user = User.query.filter_by(id=id).first()
    if not user:
        return e.not_found_error()

    try:
        db.session.delete(user)
        db.session.commit()
        data = {
            "message": "User successfully deleted."
        }
        body = json.dumps(data)

        return Response(body, status=200, mimetype='application/json')
    except DBAPIError as err:
        return e.internal_server_error()    
