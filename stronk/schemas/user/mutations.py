import graphene

from stronk import db
from stronk.models.user import User as UserModel
from stronk.schemas.user.queries import User


class CreateUser(graphene.Mutation):
    class Arguments:
        # Arguments to take went creating User
        name = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        currentProgram = graphene.Int(required=False)

    user = graphene.Field(lambda: User)

    def mutate(root, info, name, username, email, currentProgram=None):
        # TODO Get the UID from firebase token
        id = "test"
        UserModel.create(id=id,
                         name=name,
                         username=username,
                         email=email,
                         current_program=currentProgram)

        user = User(id=id,
                    name=name,
                    username=username,
                    email=email,
                    current_program=currentProgram)

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
