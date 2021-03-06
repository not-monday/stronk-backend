import graphene

from stronk.schemas.workout_exercise.type import WorkoutExercise as WorkoutExercise
from stronk.models.workout_exercise import WorkoutExercise as WorkoutExerciseModel

class AddWorkoutExercise(graphene.Mutation):
    """ adds an exercise to a workout
    """

    # mutation results
    workoutExercise = graphene.Field(WorkoutExercise)

    class Arguments:
        workout_id = graphene.Int(required=True)
        exercise_id = graphene.Int(required=True)
        superset_exercise_id = graphene.Int(required=False)
        workout_weights = graphene.List(graphene.Int, required=True)
        workout_reps = graphene.List(graphene.Int, required=True)
        rest_time = graphene.Int(required=True)

    def mutate(root, info, workout_id: str, exercise_id: str, workout_weights: int, workout_reps: int, rest_time: int, superset_exercise_id:str=None):
        workout_exercise = WorkoutExerciseModel.create(
            workout_id, exercise_id, superset_exercise_id, workout_weights, workout_reps, rest_time)
        return AddWorkoutExercise(workoutExercise=workout_exercise)


class UpdateWorkoutExercise(graphene.Mutation):
    """ updates an exercise for a workout
    """
    workoutExercise = graphene.Field(
        WorkoutExercise, description="updated workout exercise")

    class Arguments:
        workout_id = graphene.Int(required=True)
        exercise_id = graphene.Int(required=True)
        superset_exercise_id = graphene.Int(required=False)
        workout_weights = graphene.List(graphene.Int, required=False)
        workout_reps = graphene.List(graphene.Int, required=False)
        rest_time = graphene.Int(required=False)

    def mutate(root, info, workout_id, exercise_id, workout_weights, workout_reps, rest_time, superset_exercise_id:str=None):
        workout_exercise = WorkoutExerciseModel.find_workout_exercise(
            workout_id, exercise_id)
        attrs = {}
        if superset_exercise_id:
            attrs["superset_exercise_id"] = superset_exercise_id
        if workout_weights:
            attrs["workout_weights"] = workout_weights
        if workout_reps:
            attrs["workout_reps"] = workout_reps
        if rest_time:
            attrs["rest_time"] = rest_time
        workout_exercise.update(attrs)

        return UpdateWorkoutExercise(workoutExercise=workout_exercise)

class RemoveSuperSetExercise(graphene.Mutation):
    """ removes a superset from an exercise for a workout
    """
    workoutExercise = graphene.Field(WorkoutExercise)

    class Arguments:
        workout_id = graphene.Int(required=True)
        exercise_id = graphene.Int(required=True)

    def mutate(root, info, workout_id, exercise_id):
        workout_exercise = WorkoutExerciseModel.find_workout_exercise(
            workout_id, exercise_id)
        workout_exercise.removeSuperSet()

        return RemoveSuperSetExercise(workoutExercise=workout_exercise)
    
class DeleteWorkoutExercise(graphene.Mutation):
    """ deletes an exercise workout from a workout
    """
    # mutation results
    ok = graphene.Boolean()

    class Arguments:
        workout_id = graphene.Int(required=True)
        exercise_id = graphene.Int(required=True)

    def mutate(root, info, workout_id: str, exercise_id: str):
        workout_exercise = WorkoutExerciseModel.find_workout_exercise(
            workout_id, exercise_id)
        workout_exercise.delete()
        ok = True

        return DeleteWorkoutExercise(ok=ok)


class Mutation(graphene.ObjectType):
    add_workout_exercise = AddWorkoutExercise.Field()
    update_workout_exercise = UpdateWorkoutExercise.Field()
    delete_workout_exercise = DeleteWorkoutExercise.Field()
    remove_workout_superset = RemoveSuperSetExercise.Field()
