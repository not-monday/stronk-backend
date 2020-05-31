
import graphene

from stronk.errors.not_found import NotFound
from stronk.models.program_workouts import ProgramWorkouts as ProgramWorkoutsModel
from stronk.models.workout import Workout as WorkoutModel
from stronk.schemas.workout.type import Workout


class Query(graphene.ObjectType):
    workouts = graphene.List(Workout,
                             program_id=graphene.NonNull(graphene.Int))
    workout = graphene.Field(Workout,
                             id=graphene.NonNull(graphene.Int))

    def resolve_workouts(root, info, program_id: int):
        """Retrieve all workouts for a program
        """
        query = Workout.get_query(info)
        workouts = query.join(ProgramWorkoutsModel).filter(
            ProgramWorkoutsModel.program_id == program_id)
        return workouts

    def resolve_workout(root, info, id: int = None):
        """Search for a specific workout
        """
        # sqlachemy query bindings
        query = Workout.get_query(info)

        return query.filter(WorkoutModel.id == id).first()
