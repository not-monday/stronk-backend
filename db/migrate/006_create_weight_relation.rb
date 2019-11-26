class CreateWeightRelation < ActiveRecord::Migration[5.1]
    def change
      create_table :weight do |t|
        t.date :date
        t.integer :weight
        t.integer :user_id
      end

      add_foreign_key :weight, :user, column: :user_id, primary_key: "id"
    end
  end