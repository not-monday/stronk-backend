from stronk.constants import PROGRAM_NOT_FOUND_MSG, WORKOUT_NOT_FOUND_MSG, USER_NOT_FOUND_MSG

from stronk.errors.not_found import NotFound
from stronk.models.program import Program as ProgramModel
from stronk.models.program_workouts import ProgramWorkouts as ProgramWorkoutsModel
from stronk.models.workout_exercise import WorkoutExercise as WorkoutExerciseModel
from stronk.models.workout import Workout as WorkoutModel
from stronk.schemas.user.type import User


def cloneProgram(program_id: int, user_id: int):
    """duplicates a program and nested relations with the `user_id` as the author

    args:
        program_id (int): id of the program to be cloned
        user_id (int): id of the user designated to be the author of the cloned models
    """
    old_program = ProgramModel.find_by_id(program_id)
    if not old_program:
        raise NotFound(PROGRAM_NOT_FOUND_MSG)

    new_program = old_program.clone(user_id)

    # clone related relations
    old_program_workouts = ProgramWorkoutsModel.filter_by_program_id(old_program.id)
    for old_program_workout in old_program_workouts:

        # create new workout
        old_workout = WorkoutModel.find_by_id(
            old_program_workout.workout_id)
        if not old_workout:
            raise NotFound(WORKOUT_NOT_FOUND_MSG)

        new_workout = old_workout.clone(user_id)
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


def deletePrograms(user_id: int):
    """deletes all programs (and related nested models) created by the user
    note: this will not delete exercises created by the user
    """
    authored_programs = ProgramModel.find_by_author(user_id)
    for program in authored_programs:
        # delete related relations that have the user as their author
        program_workouts = ProgramWorkoutsModel.filter_by_program_id(program.id)

        for program_workout in program_workouts:

            workout = WorkoutModel.find_by_id(program_workout.workout_id)

            # delete workout exercises -> program workouts -> workouts -> programs
            workout_exercises = WorkoutExerciseModel.find_workout_exercises(workout_id=workout.id)
            for workout_exercise in workout_exercises:
                # only need to delete workout exercise, not exercise
                workout_exercise.delete()

            program_workout.delete()
            workout.delete()

        program.delete()
