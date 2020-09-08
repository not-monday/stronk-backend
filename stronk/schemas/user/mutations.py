import graphene
from firebase_admin import auth
from flask import current_app, g

from stronk.constants import USER_NOT_FOUND_MSG
from stronk.errors.not_found import NotFound
from stronk.models.user import User as UserModel
from stronk.schemas.user.type import User
from stronk.utils.auth import is_authorized


class CreateUser(graphene.Mutation):
    """Create a user."""
    # declare class attributes
    user = graphene.Field(User)

    class Arguments:
        name = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        currentProgram = graphene.Int(required=False)

    def mutate(root, info, name, username, email, currentProgram=None):
        user = UserModel.create(id=g.id,
                                name=name,
                                username=username,
                                email=email,
                                current_program=currentProgram)

        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    """Update a user given their username."""
    user = graphene.Field(User, description="User updated by this mutation.")

    class Arguments:
        username = graphene.String(required=True)
        name = graphene.String(required=False)
        email = graphene.String(required=False)
        currentProgram = graphene.Int(required=False)

    def mutate(root, info, username, name=None, email=None, currentProgram=None):
        user = UserModel.find_by_username(username)
        if not user:
            raise NotFound(USER_NOT_FOUND_MSG)
        
        is_authorized(user.id)

        attrs = {}
        if name:
            attrs["name"] = name
        if email:
            attrs["email"] = email
        if currentProgram:
            attrs["current_program"] = currentProgram
        user.update(attrs)

        return UpdateUser(user=user)


class DeleteUser(graphene.Mutation):
    """Delete a user."""
    ok = graphene.Boolean()

    class Arguments:
        username = graphene.String(required=True)

    def mutate(root, info, username):
        user = UserModel.find_by_username(username)
        if not user:
            raise NotFound(USER_NOT_FOUND_MSG)
        
        is_authorized(user.id)
        user.delete()
        ok = True

        return DeleteUser(ok=ok)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
