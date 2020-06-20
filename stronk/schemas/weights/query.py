import graphene
from flask import g

from stronk.models.weight import Weight as WeightModel
from stronk.schemas.weights.type import Weight


class Query(graphene.ObjectType):
    weights = graphene.List(Weight,
                            limit=graphene.Int())
    weight = graphene.Field(Weight,
                            measuredAt=graphene.String())

    def resolve_weights(root, info, limit: int = 5):
        """Retrieve the last 5 weights for the current user."""
        return WeightModel.get_weights_by_user_id(g.id, limit)

    def resolve_weight(root, info, measuredAt: str = None):
        """Retrieve the weight for a user by the measured date. Date should be
        in UTC."""
        return WeightModel.get_weight_by_date(g.id, measuredAt)
