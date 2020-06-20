import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from stronk.models.program import Program as ProgramModel
from stronk.models.user import User as UserModel
from stronk.models.weight import Weight as WeightModel
from stronk.schemas.program.type import Program
from stronk.schemas.weights.type import Weight


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

    # Add nested querying
    currentProgram = graphene.Field(Program)
    weights = graphene.List(Weight)

    def resolve_currentProgram(root, info):
        return ProgramModel.find_by_id(root.current_program)

    def resolve_weights(root, info, start: str = None, end: str = None):
        """Get the weight of user. Defaults to last 5 entries.
           Use the Weight GraphQL query for more entries.
        """
        return WeightModel.get_weights_by_user_id(root.id, limit=5)
