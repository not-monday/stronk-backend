from graphene_sqlalchemy import SQLAlchemyObjectType

from stronk.models.user import User as UserModel


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
