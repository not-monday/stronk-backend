import graphene
from flask import g

from stronk.constants import PROGRAM_NOT_FOUND_MSG, WORKOUT_NOT_FOUND_MSG, USER_NOT_FOUND_MSG

from stronk.errors.not_found import NotFound
from stronk.models.program import Program as ProgramModel
from stronk.models.program_workouts import ProgramWorkouts as ProgramWorkoutsModel
from stronk.models.user import User as UserModel
from stronk.models.workout_exercise import WorkoutExercise as WorkoutExerciseModel
from stronk.models.workout import Workout as WorkoutModel
from stronk.schemas.user.type import User

from stronk.utils.auth import is_authorized


class CreateUser(graphene.Mutation):
    """Create a user."""
    # declare class attributes
    user = graphene.Field(User)

    class Arguments:
        name = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        currentProgram = graphene.Int(required=False)

    def mutate(root, info, name, username, email, currentProgram=None):
        user = UserModel.create(id=g.id,
                                name=name,
                                username=username,
                                email=email,
                                current_program=currentProgram)

        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    """Update a user given their username."""
    user = graphene.Field(User, description="User updated by this mutation.")

    class Arguments:
        username = graphene.String(required=True)
        name = graphene.String(required=False)
        email = graphene.String(required=False)
        currentProgram = graphene.Int(required=False)

    def mutate(root, info, username, name=None, email=None, currentProgram=None):
        user = UserModel.find_by_username(username)
        if not user:
            raise NotFound(USER_NOT_FOUND_MSG)
        
        is_authorized(user.id)

        attrs = {}
        if name:
            attrs["name"] = name
        if email:
            attrs["email"] = email
        if currentProgram:
            if (currentProgram != -1):
                new_program = None
            else:
                new_program = _subscribeToProgram(currentProgram)
            attrs["current_program"] = new_program.id
        user.update(attrs)

        return UpdateUser(user=user)


def _subscribeToProgram(program_id: int):
    old_program = ProgramModel.find_by_id(program_id)
    if not old_program:
        raise NotFound(PROGRAM_NOT_FOUND_MSG)

    new_program = old_program.clone()

    # clone related relations
    old_program_workouts = ProgramWorkoutsModel.filter_by_program_id(old_program.id)
    for old_program_workout in old_program_workouts:

        # create new workout
        old_workout = WorkoutModel.find_by_id(
            old_program_workout.workout_id)
        if not old_workout:
            raise NotFound(WORKOUT_NOT_FOUND_MSG)

        new_workout = old_workout.clone()
        # create new program workout with the new program id and workout
        new_program_workout = old_program_workout.clone(
            new_program_id=new_program.id,
            new_workout_id=new_workout.id
        )

        old_workout_exercises = WorkoutExerciseModel.find_workout_exercises(
            workout_id=old_program_workout.workout_id)
        for old_workout_exercise in old_workout_exercises:
            old_workout_exercise.clone(new_workout_id=new_workout.id)

    return new_program


class DeleteUser(graphene.Mutation):
    """Delete a user."""
    ok = graphene.Boolean()

    class Arguments:
        username = graphene.String(required=True)

    def mutate(root, info, username):
        user = UserModel.find_by_username(username)
        if not user:
            raise NotFound(USER_NOT_FOUND_MSG)
        
        is_authorized(user.id)
        user.delete()
        ok = True

        return DeleteUser(ok=ok)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
