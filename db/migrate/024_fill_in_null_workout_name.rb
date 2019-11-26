class FillInNullWorkoutName < ActiveRecord::Migration[5.1]

    def change
        (1..6).each do |i|
            sql = "UPDATE workouts SET name = 'Program ##{i}' WHERE id = #{i}"
            ActiveRecord::Base.connection.execute(sql)
        end

    end
end
