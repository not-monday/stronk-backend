from graphene import ObjectType
from graphene_sqlalchemy import SQLAlchemyObjectType

from stronk.schemas.user_interface.type import UserInterface


class ProtectedUser(ObjectType):
    class Meta:
        interfaces = (UserInterface, )
