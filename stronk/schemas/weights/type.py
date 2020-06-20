import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from stronk.models.weight import Weight as WeightModel


class Weight(SQLAlchemyObjectType):
    class Meta:
        model = WeightModel
        exclude_fields = ('user_id', )
