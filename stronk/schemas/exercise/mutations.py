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


class UpdateExercise(graphene.Mutation):
    """Update an exercise."""
    exercise = graphene.Field(Exercise)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=False)
        desc = graphene.String(required=False)

    def mutate(root, info, id, name=None, desc=None):
        exercise = ExerciseModel.find_by_id(id)

        attrs = {}
        if name:
            attrs['name'] = name
        if desc:
            attrs['description'] = desc
        exercise.update(attrs)

        return UpdateExercise(exercise=exercise)


class DeleteExercise(graphene.Mutation):
    """Delete an exercise."""
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(root, info, id):
        ExerciseModel.find_by_id(id).delete()
        ok = True

        return DeleteExercise(ok=ok)


class Mutation(graphene.ObjectType):
    create_exercise = CreateExercise.Field()
    update_exercise = UpdateExercise.Field()
    delete_exercise = DeleteExercise.Field()
