import graphene

from stronk.constants import PROGRAM_NOT_FOUND_MSG
from stronk.errors.not_found import NotFound
from stronk.models.program import Program as ProgramModel
from stronk.models.program_workouts import ProgramWorkouts as ProgramWorkoutsModel
from stronk.models.user import User as UserModel
from stronk.schemas.program.type import Program


class CreateProgram(graphene.Mutation):
    """Create a program"""
    program = graphene.Field(Program)

    class Arguments:
        author = graphene.String(required=True)
        name = graphene.String(required=True)
        duration = graphene.Int(required=True)
        # Use desc instead of description since latter is a reserved word.
        desc = graphene.String(required=True)

    def mutate(root, info, author: str, name: str, duration: int, desc: str):
        program = ProgramModel.create(author=author,
                                      name=name,
                                      duration=duration,
                                      description=desc)
        return CreateProgram(program=program)


class UpdateProgram(graphene.Mutation):
    """Update an existing program. Throws a NotFound error if program not found.
    """
    program = graphene.Field(Program)

    class Arguments:
        id = graphene.Int(required=True)
        author = graphene.String()
        name = graphene.String()
        duration = graphene.Int()
        # Use desc instead of description since latter is a reserved word.
        desc = graphene.String()

    def mutate(root, info, id: int, author: str = None, name: str = None,
               duration: int = None, desc: str = None):
        program = ProgramModel.find_by_id(id)
        if not program:
            raise NotFound(PROGRAM_NOT_FOUND_MSG)

        attrs = {}
        if author:
            attrs['author'] = author
        if name:
            attrs['name'] = name
        if duration:
            attrs['duration'] = duration
        if desc:
            attrs['description'] = desc
        program.update(attrs)

        return UpdateProgram(program=program)


class DeleteProgram(graphene.Mutation):
    """Delete a program."""
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    def mutate(root, info, id: int):
        program = ProgramModel.find_by_id(id)
        if not program:
            raise NotFound(PROGRAM_NOT_FOUND_MSG)
        # delete program workout associations
        res = ProgramWorkoutsModel.filter_by_program_id(id)
        for r in res:
            r.delete()
        # update current program for users using program with id
        users = UserModel.find_by_program_id(id)
        for u in users:
            u.update({'current_program': None})
        program.delete()
        ok = True

        return DeleteProgram(ok=ok)


class Mutation(graphene.ObjectType):
    create_program = CreateProgram.Field()
    update_program = UpdateProgram.Field()
    delete_program = DeleteProgram.Field()
