require 'set'

class RepopulateProgramWorkout < ActiveRecord::Migration[5.1]
    
    def change
        sql = "DELETE FROM program_workout"
        ActiveRecord::Base.connection.execute(sql)

        
        program_ids = Set[1, 2, 3]
        workout_ids = Set[1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        program_ids.each do |program_id|
            sql = "INSERT INTO program_workout(program_id, workout_id) VALUES"
            used_workout_ids = Set[]
            (1..5).each do |i|
                workout_id = rand(1..9)
                while used_workout_ids.include?(workout_id)
                    workout_id = rand(1..9)
                end
                used_workout_ids.add(workout_id)

                sql += "('#{program_id}', '#{workout_id}'), "
            end

            sql = sql.slice(0, sql.length - 2) + ";"
            puts sql
            ActiveRecord::Base.connection.execute(sql)
        end
    end
end