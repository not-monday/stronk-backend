import graphene

from stronk.models.exercise import Exercise as ExerciseModel
from stronk.schemas.exercise.type import Exercise


class Query(graphene.ObjectType):
    exercises = graphene.List(Exercise, author=graphene.String())
    exercise = graphene.Field(lambda: Exercise,
                              id=graphene.Int(),
                              name=graphene.String(),
                              desc=graphene.String(),
                              author=graphene.String())

    def resolve_exercises(root, info, author=None):
        """Return a list of all exercises."""
        if author:
            return (query
                    .order_by(ExerciseModel.name.desc())
                    .filter(ExerciseModel.author == author)
                    .all())

        return Exercise.get_query(info).all()

    def resolve_exercise(root, info, id=None, name=None, desc=None, author=None):
        """Search for an exercise by id, name, author, description in decreasing
        precedence.
        """
        query = Exercise.get_query(info)
        if id:
            return query.filter(ExerciseModel.id == id).first()

        if name:
            return query.filter(ExerciseModel.name == name).first()

        if desc:
            return query.filter(ExerciseModel.description == desc).first()
