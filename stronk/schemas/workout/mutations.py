import graphene
from flask import g

from stronk.constants import PROGRAM_NOT_FOUND_MSG, WORKOUT_NOT_FOUND_MSG
from stronk.errors.not_found import NotFound

from stronk.schemas.workout.type import Workout
from stronk.schemas.workout_exercise.type import WorkoutExercise as WorkoutExercise

from stronk.models.program import Program as ProgramModel
from stronk.models.program_workouts import ProgramWorkouts as ProgramWorkoutsModel
from stronk.models.workout import Workout as WorkoutModel
from stronk.models.workout_exercise import WorkoutExercise as WorkoutExerciseModel
from stronk.utils.date import date_time_str_to_date
from stronk.utils.auth import is_authorized


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
        scheduled_time = graphene.String(required=True)

    def mutate(root, info, name: str, program_id: int, scheduled_time: str, description: str = None, projected_time: int = None):
        program = ProgramModel.find_by_id(program_id)
        if not program:
            raise NotFound(PROGRAM_NOT_FOUND_MSG)

        # convert date time string to datetime object
        formatted_time = date_time_str_to_date(scheduled_time)

        workout = WorkoutModel.create(author=g.id,
                                      name=name,
                                      description=description,
                                      projected_time=projected_time,
                                      scheduled_time=formatted_time)

        program_workout = ProgramWorkoutsModel.create(program_id=program.id,
                                                      workout_id=workout.id)
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
        scheduled_time = graphene.String(required=False)

    def mutate(root, info, id: str, name: str = None, description: str = None, projected_time: int = None, scheduled_time: str = None):
        workout = WorkoutModel.find_by_id(id)
        if not workout:
            raise NotFound(WORKOUT_NOT_FOUND_MSG)
        
        is_authorized(workout.author)

        attrs = {}
        if name:
            attrs['name'] = name
        if description:
            attrs['description'] = description
        if projected_time:
            attrs['projected_time'] = projected_time
        if scheduled_time:
            attrs['scheduled_time'] = date_time_str_to_date(scheduled_time)
        
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
        
        is_authorized(workout.author)
        # delete workout exercises associated with this workout
        WorkoutExerciseModel.deleteWorkoutExercises(id)

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
