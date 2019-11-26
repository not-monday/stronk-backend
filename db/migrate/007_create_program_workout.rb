class CreateProgramWorkout < ActiveRecord::Migration[5.1]
    def change
      create_table :program_workout, id: false do |t|
        t.integer :program_id
        t.integer :workout_id
      end

      add_foreign_key :program_id, :programs
      add_foreign_key :workout_id, :workouts
    end
  end