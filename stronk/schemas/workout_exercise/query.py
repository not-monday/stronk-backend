
import graphene

from stronk.errors.not_found import NotFound
from stronk.models.workout_exercise import WorkoutExercise as WorkoutExerciseModel
from stronk.schemas.workout_exercise.type import WorkoutExercise

class Query(graphene.ObjectType):
    workout_exercises = graphene.List(
        WorkoutExercise,
        workout_id=graphene.NonNull(graphene.Int))

    workout_exercise = graphene.Field(WorkoutExercise,
        workout_id=graphene.NonNull(graphene.Int),
        exercise_id=graphene.NonNull(graphene.Int))

    def resolve_workout_exercises(root, info, workout_id: int):
        """Retrieve all workout exercises for a given workout
        """
        return WorkoutExerciseModel.find_workout_exercises(workout_id=workout_id)

    def resolve_workout_exercise(root, info, workout_id: int, exercise_id: int):
        """Search for a specific workout exercise for a given workout 
        """
        return WorkoutExerciseModel.find_workout_exercise(workout_id=workout_id, exercise_id=exercise_id).first()
