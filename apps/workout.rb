class WorkoutApp < BaseApp
    get "/:id" do
      @workout = Workout.find_by id: params[:id]
      if @workout
        response = @workout.as_json
        exercise_ids = WorkoutExercise.where(workout_id: params[:id]).select(:exercise_id)
        exercises = []
        exercise_ids.each do |e|
          exercises << Exercise.find(e.exercise_id).as_json
        end
        response['exercises'] = exercises

        json response
      else
        response = {
          status: :fail,
          errors: [
            "Workout #{params[:id]} does not exist"
          ],
          data: [],
          request: params,
          redirect: nil
        }
        json response
      end
    end
    
    get "/" do
      json Workout.all.as_json
    end

    post '/' do
      @workout = Workout.create username: @body[:username],
                          password: @body[:password],
                          email: @body[:email]
      if @workout.valid?
        json response: {
          status: :ok,
          errors: [],
          data: @workout,
          request: @body,
          redirect: "/#{@workout.id}"
        }
      else
        json response: {
          status: :fail,
          errors: @workout.errors,
          data: [],
          request: @body,
          redirect: "/"
        }
      end
    end
  end