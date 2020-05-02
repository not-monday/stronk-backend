import graphene

from stronk import db
from stronk.models.user import User as UserModel
from stronk.schemas.user.queries import User


class CreateUser(graphene.Mutation):
    ok = graphene.Boolean()
    user = graphene.Field(User)

    class Arguments:
        # Arguments to take went creating User
        # id = graphene.Int(required=True)
        name = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        currentProgram = graphene.Int(required=False)

    # def mutate(root, info, id, name, username, email, currentProgram=None):
    def mutate(root, info, name, username, email, currentProgram=None):
        u = UserModel(name=name,
                      username=username,
                      email=email,
                      current_program=currentProgram)
        if currentProgram:
            u.current_program = currentProgram

        db.session.add(u)
        db.session.commit()

        user = User(id=id,
                    name=name, username=username,
                    email=email,
                    current_program=currentProgram)

        ok = True
        return CreateUser(user=user, ok=ok)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
