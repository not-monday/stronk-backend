class CreatePrograms < ActiveRecord::Migration[5.1]
    def up
      create_table :programs do |t|
        t.string :author
        t.integer :duration
        t.string :description
      end
    end
  
    def down
      drop_table :programs
    end
  end