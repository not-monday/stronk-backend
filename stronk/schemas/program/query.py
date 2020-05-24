import graphene

from stronk.models.program import Program as ProgramModel
from stronk.schemas.program.type import Program


class Query(graphene.ObjectType):
    programs = graphene.List(Program)
    program = graphene.Field(Program,
                             id=graphene.Int(),
                             name=graphene.String(),
                             author=graphene.String())

    def resolve_programs(root, info):
        query = Program.get_query(info)
        return query.all()

    def resolve_program(root, info, id: int = None, name: str = None, author: str = None):
        """Search for program in decreasing order of precedence: id, name and
           author. If an author created more than one program, a list of
           programs is returned."""
        query = Program.get_query(info)
        if id:
            return query.filter(ProgramModel.id == id).first()

        if name:
            return query.filter(ProgramModel.name == name).first()

        if author:
            return query.filter(ProgramModel.author == author).first()

        return None
