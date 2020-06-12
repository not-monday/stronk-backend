import graphene

from stronk.constants import WORKOUT_EXERCISE_NOT_FOUND_MSG
from stronk.errors.not_found import NotFound

from stronk.schemas.exercise.type import WorkoutExercise as WorkoutExercise
from stronk.models.workout_exercise import WorkoutExercise as WorkoutExerciseModel

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
        workout_weights = graphene.List(graphene.Int, required=False)
        workout_reps = graphene.List(graphene.Int, required=False)
        rest_time = graphene.List(graphene.Int, required=False)

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

        return RemoveWorkoutExercise(ok=ok)


class Mutation(graphene.ObjectType):
    add_workout_exercise = AddWorkoutExercise.Field()
    update_workout_exercise = UpdateWorkoutExercise.Field()
    remove_workout_exercise = RemoveWorkoutExercise.Field()
