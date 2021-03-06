import graphene

from stronk.schemas.exercise.mutations import Mutation as ExerciseMutation
from stronk.schemas.exercise.query import Query as ExerciseQuery
from stronk.schemas.program.mutations import Mutation as ProgramMutation
from stronk.schemas.program.query import Query as ProgramQuery
from stronk.schemas.program_reviews.mutations import Mutation as ProgramReviewsMutation
from stronk.schemas.program_reviews.query import Query as ProgramReviewsQuery
from stronk.schemas.user.mutations import Mutation as UserMutation
from stronk.schemas.user.query import Query as UserQuery
from stronk.schemas.weights.query import Query as WeightQuery
from stronk.schemas.weights.mutation import Mutation as WeightMutation
from stronk.schemas.workout.mutations import Mutation as WorkoutMutation
from stronk.schemas.workout.query import Query as WorkoutQuery
from stronk.schemas.workout_exercise.mutations import Mutation as WorkoutExerciseMutation
from stronk.schemas.workout_exercise.query import Query as WorkoutExerciseQuery
# Concrete objects for graphql interfaces
from stronk.schemas.user.type import User
from stronk.schemas.protected_user.type import ProtectedUser


class Query(ProgramQuery,
            ProgramReviewsQuery,
            WeightQuery,
            WorkoutQuery,
            WorkoutExerciseQuery,
            ExerciseQuery,
            UserQuery,
            graphene.ObjectType):
    pass


class Mutation(ProgramMutation,
               ProgramReviewsMutation,
               WeightMutation,
               WorkoutMutation,
               WorkoutExerciseMutation,
               ExerciseMutation,
               UserMutation,
               graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation,
                         types=[User, ProtectedUser])
