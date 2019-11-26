class PopulateProgramWorkout < ActiveRecord::Migration[5.1]
    
    def change
        sql = "INSERT INTO program_workout(program_id, workout_id) VALUES"
        
        (1..20).each do |i|
            sql += "('#{rand(1..3)}', '#{rand(1..9)}'), "
        end
        
        sql = sql.slice(0, sql.length - 2) + ";"
        puts sql

        records_array = ActiveRecord::Base.connection.execute(sql)
    end
end