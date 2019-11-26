class PopulateWorkoutExercise < ActiveRecord::Migration[5.1]
    
    def change
        sql = "INSERT INTO workout_exercise(workout_id, exercise_id) VALUES"
        
        (1..20).each do |i|
            sql += "('#{rand(1..9)}', '#{rand(1..5)}'), "
        end
        
        sql = sql.slice(0, sql.length - 2) + ";"
        puts sql

        records_array = ActiveRecord::Base.connection.execute(sql)
    end
  end