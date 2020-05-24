import graphene

from stronk.models.user import User as UserModel
from stronk.schemas.user.type import User


class Query(graphene.ObjectType):
    users = graphene.List(User)
    user = graphene.Field(lambda: User,
                          id=graphene.String(),
                          username=graphene.String(),
                          email=graphene.String(),
                          currentProgram=graphene.Int())

    def resolve_users(root, info):
        query = User.get_query(info)
        return query.all()

    def resolve_user(root, info, id=None, username=None, email=None, currentProgram=None):
        """Search for user in decreasing order of precedence: id, username,
        email and current program.
        """
        query = User.get_query(info)
        if id:
            return query.filter(UserModel.id == id).first()

        if username:
            return query.filter(UserModel.username == username).first()

        if email:
            return query.filter(UserModel.email == email).first()

        if currentProgram:
            return query.filter(UserModel.current_program == currentProgram).first()

        return None
