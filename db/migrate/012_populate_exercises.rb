class PopulateExercises < ActiveRecord::Migration[5.1]
    
    def change
        add_column :exercises, :name, :string

        sql = "INSERT INTO exercises(name, description) VALUES"
        names = ["Push Ups", "Planks", "Squats", "Chin Ups", "Brench Press"]
        description = ["A push-up is a common calisthenics exercise beginning from the prone position.",
                        "The plank is an isometric core strength exercise that involves maintaining a position similar to a push-up for the maximum possible time.",
                        "A squat is a strength exercise in which the trainee lowers their hips from a standing position and then stands back up",
                        "Done with both hands in an overhand (or prone) grip slightly wider than shoulder-width apart, prove to be the most difficult of the pair.",
                        "The bench press is a core fundamental exercise for developing upper body strength."]
        names.each_with_index do |name, i|
            sql += "('#{name}', '#{description[i]}'), "
        end
        
        sql = sql.slice(0, sql.length - 2) + ";"
        puts sql

        records_array = ActiveRecord::Base.connection.execute(sql)
    end
  end