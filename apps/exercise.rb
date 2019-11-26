class ExerciseApp < BaseApp
    get "/:id" do
      @exercise = Exercise.find_by id: params[:id]
      if @exercise
        json @exercise.as_json
      else
        response = {
          status: :fail,
          errors: [
            "Exercise #{params[:id]} does not exist"
          ],
          data: [],
          request: params,
          redirect: nil
        }
        json response
      end
    end
    
    get "/" do
      json Exercise.all
    end

    post '/' do
      @exercise = Exercise.create username: @body[:username],
                          password: @body[:password],
                          email: @body[:email]
      if @exercise.valid?
        response = {
          status: :ok,
          errors: [],
          data: @exercise,
          request: @body,
          redirect: "/#{@exercise.id}"
        }
        json response
      else
        response = {
          status: :fail,
          errors: @exercise.errors,
          data: [],
          request: @body,
          redirect: "/"
        }
        json response
      end
    end
  end