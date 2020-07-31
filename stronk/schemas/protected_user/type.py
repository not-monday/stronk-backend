from graphene import ObjectType
from graphene_sqlalchemy import SQLAlchemyObjectType

from stronk.models.user import User as UserModel
from stronk.schemas.user_interface.type import UserInterface


class ProtectedUser(ObjectType):
    class Meta:
        interfaces = (UserInterface, )
