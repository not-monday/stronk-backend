class CreateExerciseTracking < ActiveRecord::Migration[5.1]
    def change
      create_table :exercise_tracking, id: false do |t|
        t.integer :user_id
        t.integer :exercise_id
        t.date :date
        t.integer :weight
        t.integer :reps
      end

      add_foreign_key :exercise_tracking, :users, column: :user_id, primary_key: "id"
      add_foreign_key :exercise_tracking, :exercises, column: :exercise_id, primary_key: "id"
    end
  end