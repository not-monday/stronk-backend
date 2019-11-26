require 'set'

class RepopulateWorkoutExercise < ActiveRecord::Migration[5.1]
    
    def change
        sql = "DELETE FROM workout_exercise"
        ActiveRecord::Base.connection.execute(sql)

        
        workout_ids = Set[1, 2, 3, 4, 5, 6, 7, 8, 9]
        exercise_ids = Set[1, 2, 3, 4, 5]
        
        workout_ids.each do |workout_id|
            sql = "INSERT INTO workout_exercise(workout_id, exercise_id) VALUES"
            used_exercise_ids = Set[]
            (1..5).each do |i|
                exercise_id = rand(1..5)
                while used_exercise_ids.include?(exercise_id)
                    exercise_id = rand(1..5)
                end
                used_exercise_ids.add(exercise_id)

                sql += "('#{workout_id}', '#{exercise_id}'), "
            end

            sql = sql.slice(0, sql.length - 2) + ";"
            puts sql
            ActiveRecord::Base.connection.execute(sql)
        end
    end
end