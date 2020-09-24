import graphene

from stronk.models.exercise import Exercise as ExerciseModel
from stronk.models.user import User as UserModel
from stronk.schemas.exercise.type import Exercise


class Query(graphene.ObjectType):
    exercises = graphene.List(Exercise, author=graphene.String())
    exercise = graphene.Field(lambda: Exercise,
                              id=graphene.Int())

    def resolve_exercises(root, info, author=None):
        """Return a list of all exercises.

           Search by author: A user's username.
        """
        query = Exercise.get_query(info)
        if author:
            user = UserModel.find_by_username(author)
            return (query
                    .order_by(ExerciseModel.name.desc())
                    .filter(ExerciseModel.author == user.id)
                    .all())

        return query.all()

    def resolve_exercise(root, info, id=None, name=None, desc=None):
        """Return a single exercise by id.
        """
        query = Exercise.get_query(info)
        if id:
            return query.filter(ExerciseModel.id == id).first()
        return None