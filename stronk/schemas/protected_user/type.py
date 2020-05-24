from graphene_sqlalchemy import SQLAlchemyObjectType

from stronk.models.user import User as UserModel


class ProtectedUser(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        # `currentProgram` in GraphQL query is `current_program` in UserModel
        exclude_fields = ('id', 'current_program', 'email', )
