from graphene import ObjectType
from stronk.schemas.user_interface.type import UserInterface


class ProtectedUser(ObjectType):
    class Meta:
        interfaces = (UserInterface, )
