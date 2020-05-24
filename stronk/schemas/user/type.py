import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from stronk.models.program import Program as ProgramModel
from stronk.models.user import User as UserModel
from stronk.schemas.program.type import Program


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

    # Add nested querying
    currentProgram = graphene.Field(Program)

    def resolve_currentProgram(root, info):
        return ProgramModel.find_by_id(root.current_program)
