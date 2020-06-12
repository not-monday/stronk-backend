import graphene

from stronk.constants import PROGRAM_NOT_FOUND_MSG, WORKOUT_NOT_FOUND_MSG, WORKOUT_EXERCISE_NOT_FOUND_MSG
from stronk.errors.not_found import NotFound

from stronk.schemas.workout.type import Workout
from stronk.schemas.exercise.type import WorkoutExercise as WorkoutExercise

from stronk.models.program import Program as ProgramModel
from stronk.models.program_workouts import ProgramWorkouts as ProgramWorkoutsModel
from stronk.models.workout import Workout as WorkoutModel
from stronk.models.workout_exercise import WorkoutExercise as WorkoutExerciseModel


class CreateWorkout(graphene.Mutation):
    """ creates a workout and adds it to a program - result is the new workout
    """
    # mutation results
    workout = graphene.Field(Workout)

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=False)
        projected_time = graphene.Int(required=False)
        program_id = graphene.Int(required=True)

    def mutate(root, info, name: str, program_id: int, description: str = None, projected_time: int = None):
        program = ProgramModel.find_by_id(program_id)
        if not program:
            raise NotFound(PROGRAM_NOT_FOUND_MSG)

        workout = WorkoutModel.create(
            name=name, description=description, projected_time=projected_time)

        program_workout = ProgramWorkoutsModel.create(
            program_id=program.id, workout_id=workout.id)
        return CreateWorkout(workout=workout)


class UpdateWorkout(graphene.Mutation):
    """ updates a workout's information
    """
    # mutation results
    workout = graphene.Field(Workout)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=False)
        description = graphene.String(required=False)
        projected_time = graphene.Int(required=False)

    def mutate(root, info, id: str, name: str = None, description: str = None, projected_time: int = None):
        workout = WorkoutModel.find_by_id(id)
        if not workout:
            raise NotFound(WORKOUT_NOT_FOUND_MSG)

        attrs = {}
        if name:
            attrs['name'] = name
        if description:
            attrs['description'] = description
        if projected_time:
            attrs['projected_time'] = projected_time
        workout.update(attrs)

        return UpdateWorkout(workout=workout)


class DeleteWorkout(graphene.Mutation):
    """ removes a workout from a program
    """
    # mutation results
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int()

    def mutate(root, info, id):
        workout = WorkoutModel.find_by_id(id)
        if not workout:
            raise NotFound(WORKOUT_NOT_FOUND_MSG)

        # each workout should be unique to a program
        program_workout = ProgramWorkoutsModel.find_by_workout_id(id)
        program_workout.delete()

        workout.delete()
        ok = True

        return DeleteWorkout(ok=ok)


class AddWorkoutExercise(graphene.Mutation):
    """ adds an exercise to a workout
    """

    # mutation results
    workoutExercise = graphene.Field(WorkoutExercise)

    class Arguments:
        workout_id = graphene.Int(required=True)
        exercise_id = graphene.Int(required=True)
        workout_weights = graphene.List(graphene.Int, required=True)
        workout_reps = graphene.List(graphene.Int, required=True)
        rest_time = graphene.List(graphene.Int, required=True)

    def mutate(root, info, workout_id: str, exercise_id: str, workout_weights: int, workout_reps: int, rest_time: int):
        workoutExercise = WorkoutExerciseModel.create(
            workout_id, exercise_id, workout_weights, workout_reps, rest_time)
        return AddWorkoutExercise(workoutExercise=workoutExercise)


class UpdateWorkoutExercise(graphene.Mutation):
    """ updates an exercise for a workout
    """
    workoutExercise = graphene.Field(
        WorkoutExercise, description="updated workout exercise")

    class Arguments:
        workout_id = graphene.Int(required=True)
        exercise_id = graphene.Int(required=True)
        workout_weights = graphene.List(graphene.Int, required=True)
        workout_reps = graphene.List(graphene.Int, required=True)
        rest_time = graphene.List(graphene.Int, required=True)

    def mutate(root, info, workout_id, exercise_id, workout_weights, workout_reps, rest_time):
        workoutExercise = WorkoutExerciseModel.find_workout_exercise(
            workout_id, exercise_id)
        if not workoutExercise:
            raise NotFound(WORKOUT_EXERCISE_NOT_FOUND_MSG)

        attrs = {}
        if workout_weights:
            attrs["workout_weights"] = workout_weights
        if workout_reps:
            attrs["workout_reps"] = workout_reps
        if rest_time:
            attrs["rest_time"] = rest_time
        workoutExercise.update(attrs)

        return UpdateWorkoutExercise(workoutExercise=workoutExercise)


class RemoveWorkoutExercise(graphene.Mutation):
    """ removes an exercise from a workout
    """
    # mutation results
    ok = graphene.Boolean()

    class Arguments:
        workout_id = graphene.Int(required=True)
        exercise_id = graphene.Int(required=True)

    def mutate(root, info, workout_id: str, exercise_id: str):
        workoutExercise = WorkoutExerciseModel.find_workout_exercise(
            workout_id, exercise_id)
        if not workoutExercise:
            raise NotFound(WORKOUT_EXERCISE_NOT_FOUND_MSG)

        workoutExercise.delete()
        ok = True

        return DeleteWorkout(ok=ok)


class Mutation(graphene.ObjectType):
    create_workout = CreateWorkout.Field()
    update_workout = UpdateWorkout.Field()
    delete_workout = DeleteWorkout.Field()
    # workout exercises
    add_workout_exercise = AddWorkoutExercise.Field()
    update_workout_exercise = UpdateWorkoutExercise.Field()
    remove_workout_exercise = RemoveWorkoutExercise.Field()
