class AddUserProgramForeignKey < ActiveRecord::Migration[5.1]
    def change
        add_column :users, :current_program, :string
        add_foreign_key :users, :programs, column: :current_program, primary_key: "id"
    end
  end