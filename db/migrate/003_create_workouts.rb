class CreateWorkouts < ActiveRecord::Migration[5.1]
    def up
      create_table :workouts do |t|
        t.string :description
        t.integer :projected_time
      end
    end
  
    def down
      drop_table :workouts
    end
  end