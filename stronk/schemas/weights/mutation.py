import graphene
from flask import g

from stronk.constants import WEIGHT_NOT_FOUND_MSG
from stronk.errors.not_found import NotFound
from stronk.models.weight import Weight as WeightModel
from stronk.schemas.weights.type import Weight


class AddWeight(graphene.Mutation):
    """Create a weight record for a user"""
    weight = graphene.Field(Weight)

    class Arguments:
        weight = graphene.Float(required=True)

    def mutate(root, info, weight: float):
        weight = WeightModel.create(g.id, weight)

        return AddWeight(weight=weight)


class UpdateWeight(graphene.Mutation):
    """Update a weight record for a user given a new weight and date measured."""
    weight = graphene.Field(Weight)

    class Arguments:
        weight = graphene.Float(required=True)
        measured_at = graphene.String(required=True)

    def mutate(root, info, weight: float, measured_at: str):
        w = WeightModel.get_weight_by_date(g.id, measured_at)
        if not w:
            raise NotFound(WEIGHT_NOT_FOUND_MSG)

        attrs = {'weight': weight}
        w.update(attrs)

        return UpdateWeight(weight=w)


class DeleteWeight(graphene.Mutation):
    """Delete a weight record for a user"""
    ok = graphene.Boolean()

    class Arguments:
        measured_at = graphene.String(required=True)

    def mutate(root, info, measured_at: str):
        w = WeightModel.get_weight_by_date(g.id, measured_at)
        if not w:
            raise NotFound(WEIGHT_NOT_FOUND_MSG)

        w.delete()
        ok = True

        return DeleteWeight(ok=ok)


class Mutation(graphene.ObjectType):
    add_weight = AddWeight.Field()
    update_weight = UpdateWeight.Field()
    delete_weight = DeleteWeight.Field()
