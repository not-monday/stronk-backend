class UserApp < BaseApp
    get "/:id" do
      @user = User.find_by id: params[:id]
      if @user
        weights = Weight.where(user_id: params[:id])
        response = @user.as_json
        response['program'] = Program.find(@user.current_program) 
        json response
      else
        response = {
          status: :fail,
          errors: [
            "User #{params[:id]} does not exist"
          ],
          data: [],
          request: params,
          redirect: nil
        }
        json response
      end
    end
    
    get "/" do
      json User.all
    end

    post '/' do
      @user = User.create username: @body[:username],
                          password: @body[:password],
                          email: @body[:email]
      if @user.valid?
        json response: {
          status: :ok,
          errors: [],
          data: @user,
          request: @body,
          redirect: "/#{@user.id}"
        }
      else
        json response: {
          status: :fail,
          errors: @user.errors,
          data: [],
          request: @body,
          redirect: "/"
        }
      end
    end
  end