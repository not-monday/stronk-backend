import graphene

from stronk.schemas.workout.type import Workout as WorkoutType

from stronk.models.program import Program as ProgramModel
from stronk.models.program_workouts import ProgramWorkouts as ProgramWorkoutsModel
from stronk.models.workout import Workout as WorkoutModel

from werkzeug.exceptions import NotFound


class CreateWorkout(graphene.Mutation):
    """ creates a workout and adds it to a program - result is the new workout
    """
    # mutation results
    workout = graphene.Field(WorkoutType)

    class Arguments:
        name = graphene.String()
        description = graphene.String()
        projected_time = graphene.Int()
        program_id = graphene.Int()

    def mutate(root, info, name: str, description: str, projected_time: int, program_id: int):
        program = ProgramModel.find_by_id(program_id)
        if not program:
            raise NotFound("Program not found.")

        workout = WorkoutModel.create(
            name=name, description=description, projected_time=projected_time, programId=program_id)

        program_workout = ProgramWorkoutsModel.create(program_id=program.id, workout_id=workout.id)
        return CreateWorkout(workout=workout)

class UpdateWorkout(graphene.Mutation):
    """ updates a workout's information
    """
    # mutation results
    workout = graphene.Field(WorkoutType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=False)
        description = graphene.String(required=False)
        projected_time = graphene.Int(required=False)

    def mutate(root, info, id: str, name: str, description: str, projected_time: int):
        workout = WorkoutModel.find_by_id(id)
        if not workout:
            raise NotFound("Workout not found.")

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
            raise NotFound("Workout not found.")

        # each workout should be unique to a program
        program_workout = ProgramWorkoutsModel.find_by_workout_id(id)
        program_workout.delete()

        workout.delete()
        ok = True

        return DeleteWorkout(ok=ok)


class Mutation(graphene.ObjectType):
    create_workout = CreateWorkout.Field()
    update_workout = UpdateWorkout.Field()
    delete_workout = DeleteWorkout.Field()