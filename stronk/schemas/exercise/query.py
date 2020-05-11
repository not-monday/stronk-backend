import graphene

from stronk.models.exercise import Exercise as ExerciseModel
from stronk.schemas.exercise.type import Exercise


class Query(graphene.ObjectType):
    exercises = graphene.List(Exercise)
    exercise = graphene.Field(lambda: Exercise,
                              id=graphene.Int(),
                              name=graphene.String(),
                              desc=graphene.String())

    def resolve_exercises(root, info):
        """Return a list of all exercises."""
        return Exercise.get_query(info).all()

    def resolve_exercise(root, info, id=None, name=None, desc=None):
        """Search for an exercise by id, name, description in decreasing
        precedence.
        """
        query = Exercise.get_query(info)
        if id:
            return query.filter(ExerciseModel.id == id).first()

        if name:
            return query.filter(ExerciseModel.name == name).first()

        if desc:
            return query.filter(ExerciseModel.description == desc).first()

        return None
