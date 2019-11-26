class CreateProgramReview < ActiveRecord::Migration[5.1]
    def change
      create_table :program_reviews do |t|
        t.integer :program_id
        t.string :author
        t.integer :rating
        t.string :review
      end

      add_foreign_key :program_reviews, :programs, column: :program_id, primary_key: "id"
      add_foreign_key :program_reviews, :users, column: :author, primary_key: "id"
    end
  end