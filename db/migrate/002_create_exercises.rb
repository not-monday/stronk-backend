class CreateExercises < ActiveRecord::Migration[5.1]
    def up
      create_table :exercises do |t|
        t.string :description
      end
    end
  
    def down
      drop_table :exercises
    end
  end