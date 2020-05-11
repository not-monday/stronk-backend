import graphene

from stronk.models.exercise import Exercise as ExerciseModel
from stronk.schemas.exercise.type import Exercise


class CreateExercise(graphene.Mutation):
    """Create an exercise."""
    # declare class attributes
    exercise = graphene.Field(Exercise)

    class Arguments:
        name = graphene.String(required=True)
        # Use desc instead of description since latter is a reserved word.
        desc = graphene.String(required=True)

    def mutate(root, info, name, desc):
        exercise = ExerciseModel.create(name=name, description=desc)

        return CreateExercise(exercise=exercise)


class Mutation(graphene.ObjectType):
    create_exercise = CreateExercise.Field()
