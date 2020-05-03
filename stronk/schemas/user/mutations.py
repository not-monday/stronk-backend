import graphene
from firebase_admin import auth
from flask import g

from stronk import db
from stronk.models.user import User as UserModel
from stronk.schemas.user.type import User


class CreateUser(graphene.Mutation):
    # declare class attributes
    user = graphene.Field(User)

    class Arguments:
        # Arguments to take went creating User
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


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
