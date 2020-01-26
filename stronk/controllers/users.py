"""Contains the Blueprint for users routes."""
import json
from flask import Blueprint, request, Response
from sqlalchemy.exc import DBAPIError
from stronk.models.user import User
from stronk.errors import api_errors as e

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
    # Parse request body
    # Create user object
    # Save it in the db
    req_body = request.get_json()
    return "Adding new user with data: " + str(req_body)

# PATCH /users/:id
@users_page.route('/<int:id>', methods=['PATCH'])
def update_user(id):
    # Use ORM to fetch user
    # Use ORM to update user
    # Use ORM to save the user
    return "Update user " + str(id)

# DELETE /users/:id
@users_page.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    # User ORM to fetch the user (if exists)
    # Delete the user if it exists
    return "Deleting user " + str(id)
