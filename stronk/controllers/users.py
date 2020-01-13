"""Contains the Blueprint for users routes."""
from flask import Blueprint, request

users_page = Blueprint('users', __name__)

# GET /users
@users_page.route('/', methods=['GET'])
def get_users():
    return "Showing All Users"

# GET /users/:id
@users_page.route('/<int:id>', methods=['GET'])
def get_user(id):
    return "Showing user " + str(id)

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
