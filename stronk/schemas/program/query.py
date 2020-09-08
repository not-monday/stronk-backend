import graphene

from stronk.models.program import Program as ProgramModel
from stronk.models.user import User as UserModel
from stronk.schemas.program.type import Program
from stronk.errors.not_found import NotFound
from stronk.constants import USER_NOT_FOUND_MSG

class Query(graphene.ObjectType):
    programs = graphene.List(Program, author=graphene.String())
    program = graphene.Field(Program,
                             id=graphene.Int(),
                             name=graphene.String())

    def resolve_programs(root, info, author=None):
        """Return a list of programs.

           Search by author: A user's username.
        """
        query = Program.get_query(info)

        if author:
            user = UserModel.find_by_username(author)
            if not user:
                raise NotFound(USER_NOT_FOUND_MSG)

            return (query
                    .order_by(ProgramModel.name.desc())
                    .filter(ProgramModel.author == user.id)
                    .all())

        return query.all()

    def resolve_program(root, info, id: int = None, name: str = None):
        """Search for program in decreasing order of precedence: id, name."""
        query = Program.get_query(info)
        if id:
            return query.filter(ProgramModel.id == id).first()

        if name:
            return query.filter(ProgramModel.name == name).first()

        return None
