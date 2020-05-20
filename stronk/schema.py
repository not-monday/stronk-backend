import graphene

from stronk.models.user import User as UserModel
from stronk.schemas.exercise.mutations import Mutation as ExerciseMutation
from stronk.schemas.exercise.query import Query as ExerciseQuery
from stronk.schemas.user.mutations import Mutation as UserMutation
from stronk.schemas.user.queries import Query as UserQuery
from stronk.schemas.workout.mutations import Mutation as WorkoutMutation
from stronk.schemas.workout.query import Query as WorkoutQuery


class Query(WorkoutQuery, ExerciseQuery, UserQuery, graphene.ObjectType):
    pass


class Mutation(WorkoutMutation, ExerciseMutation, UserMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
