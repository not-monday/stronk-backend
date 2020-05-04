import graphene
from firebase_admin import auth
from flask import g

from stronk import db
from stronk.models.user import User as UserModel
from stronk.schemas.user.type import User


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
        id = auth.get_user(g.get("firebase_token"))
        user = UserModel.create(id=id,
                                name=name,
                                username=username,
                                email=email,
                                current_program=currentProgram)

        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    """Update a user."""
    user = graphene.Field(User, description="User updated by this mutation.")

    class Arguments:
        id = graphene.String(required=True)
        name = graphene.String(required=False)
        username = graphene.String(required=False)
        email = graphene.String(required=False)
        currentProgram = graphene.Int(required=False)

    def mutate(root, info, id, name=None, username=None, email=None,
               currentProgram=None):
        user = UserModel.find_by_id(id)

        attrs = {}
        if name:
            attrs["name"] = name
        if username:
            attrs["username"] = username
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
        id = graphene.String(required=True)

    def mutate(root, info, id):
        UserModel.find_by_id(id).delete()
        ok = True

        return DeleteUser(ok=ok)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
