import graphene
from flask import g

from stronk.constants import USER_NOT_FOUND_MSG
from stronk.errors.not_found import NotFound
from stronk.models.user import User as UserModel
from stronk.schemas.protected_user.type import ProtectedUser
from stronk.schemas.user.type import User
from stronk.schemas.user_interface.type import UserInterface


class Query(graphene.ObjectType):
    user = graphene.Field(
        UserInterface, username=graphene.String(required=True))
    users = graphene.List(UserInterface)

    def resolve_users(root, info):
        """Returns UserInterface[] information about all users.
        Other users are type ProtectedUser whereas the user itself is type User.
        """
        users = User.get_query(info).all()
        result = []
        for user in users:
            if user.id == g.id:
                result.append(user)
            else:
                result.append(ProtectedUser(
                    name=user.name, username=user.username))

        return result

    def resolve_user(root, info, username):
        """Returns user's information based on the username.
        Other users are returned as type ProtectedUser whereas the user itself
        is type User.
        """
        u = UserModel.find_by_username(username)
        if not u:
            raise NotFound(USER_NOT_FOUND_MSG)

        return u if u.id == g.id else ProtectedUser(name=u.name,
                                                    username=u.username)
