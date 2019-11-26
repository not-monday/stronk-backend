class CreateWorkoutExercise < ActiveRecord::Migration[5.1]
    def change
      create_table :workout_exercise, id: false do |t|
        t.integer :workout_id
        t.integer :exercise_id
      end
    end

    add_foreign_key :workout_exercise, :workouts, column: :workout_id, primary_key: "id"
    add_foreign_key :workout_exercise, :exercise, column: :exercise_id, primary_key: "id"
  end