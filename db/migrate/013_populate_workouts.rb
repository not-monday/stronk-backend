class PopulateWorkouts < ActiveRecord::Migration[5.1]
    
    def change
        add_column :workouts, :name, :string

        sql = "INSERT INTO workouts(name, description, projected_time) VALUES"
        names = ["Easy Workout", "Medium Workout", "Hard Workout"]
        description = ["An easy workout to get started.",
                        "A medium workout that is a little more difficult than easy.",
                        "A hard workout that is really difficult."]
        projected_times = [30, 45, 50]
        names.each_with_index do |name, i|
            sql += "('#{name}', '#{description[i]}', #{projected_times[i]}), "
        end
        
        sql = sql.slice(0, sql.length - 2) + ";"
        puts sql

        records_array = ActiveRecord::Base.connection.execute(sql)
    end
  end