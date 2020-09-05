from stronk.constants import PROGRAM_NOT_FOUND_MSG, WORKOUT_NOT_FOUND_MSG, USER_NOT_FOUND_MSG

from stronk.errors.not_found import NotFound
from stronk.models.program import Program as ProgramModel
from stronk.models.program_workouts import ProgramWorkouts as ProgramWorkoutsModel
from stronk.models.workout_exercise import WorkoutExercise as WorkoutExerciseModel
from stronk.models.workout import Workout as WorkoutModel
from stronk.schemas.user.type import User


def subscribeToProgram(program_id: int):
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
