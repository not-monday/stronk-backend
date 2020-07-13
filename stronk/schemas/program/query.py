import graphene

from stronk.models.program import Program as ProgramModel
from stronk.models.user import User as UserModel
from stronk.schemas.program.type import Program
from stronk.errors.not_found import NotFound
from stronk.constants import USER_NOT_FOUND_MSG

class Query(graphene.ObjectType):
    programs = graphene.List(Program)
    program = graphene.Field(Program,
                             id=graphene.Int(),
                             name=graphene.String(),
                             author=graphene.String())

    def resolve_programs(root, info):
        query = Program.get_query(info)
        return query.all()

    def resolve_program(root, info, id: int = None, name: str = None, author: str = None, user_id:int = None, ):
        """Search for program in decreasing order of precedence: id, name, author,
           and user id. If an author created more than one program, a list of
           programs is returned."""
        query = Program.get_query(info)
        if id:
            return query.filter(ProgramModel.id == id).first()

        if name:
            return query.filter(ProgramModel.name == name).first()

        if author:
            return query.filter(ProgramModel.author == author).first()

        if user_id:
            user : UserModel = UserModel.find_by_id(user_id)
            if not user:
                raise NotFound(USER_NOT_FOUND_MSG)

            return query.filter(ProgramModel.id == user.current_program).first()

        return None
