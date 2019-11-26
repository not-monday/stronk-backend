class ProgramApp < BaseApp
    get "/:id" do
      @program = Program.find_by id: params[:id]
      if @program
        response = @program.as_json
        workout_ids = ProgramWorkout.where(program_id: params[:id]).select(:workout_id)

        workouts = []
        workout_ids.each do |w|
          workouts << Workout.find(w.workout_id).as_json
        end
        response['workouts'] = workouts

        json response
      else
        response = {
          status: :fail,
          errors: [
            "Program #{params[:id]} does not exist"
          ],
          data: [],
          request: params,
          redirect: nil
        }
        json response
      end
    end
    
    get "/" do
      json Program.all.as_json
    end

    post '/' do
      @program = Program.create username: @body[:username],
                          password: @body[:password],
                          email: @body[:email]
      if @program.valid?
        json response: {
          status: :ok,
          errors: [],
          data: @program,
          request: @body,
          redirect: "/#{@program.id}"
        }
      else
        json response: {
          status: :fail,
          errors: @program.errors,
          data: [],
          request: @body,
          redirect: "/"
        }
      end
    end
  end