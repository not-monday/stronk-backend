
import graphene

from stronk.models.program_workouts import ProgramWorkouts as ProgramWorkoutsModel
from stronk.models.workout import Workout as WorkoutModel

from stronk.schemas.workout.type import Workout as WorkoutType
from stronk.schemas.workout.type import ProgramWorkouts as ProgramWorkoutsType

from werkzeug.exceptions import BadRequest, NotFound


class Query(graphene.ObjectType):
    workouts = graphene.List(WorkoutType,
                             programId=graphene.NonNull(graphene.Int))
    workout = graphene.Field(WorkoutType,
                             id=graphene.NonNull(graphene.Int))

    def resolve_workouts(root, info, programId: int):
        """Retrieve all workouts for a program
        """
        query = WorkoutType.get_query(info)
        workouts = query.join(ProgramWorkoutsModel).filter(
            ProgramWorkoutsModel.program_id == programId)
        return workouts

    def resolve_workout(root, info, id: int = None):
        """Search for a specific workout
        """
        # sqlachemy query bindings
        query = WorkoutType.get_query(info)

        # TODO check for permissions for each workout
        return query.filter(WorkoutModel.id == id).first()
