class ChangeAuthorFromStringToInt < ActiveRecord::Migration[5.1]
    
    def change
        change_column :programs, :author, :integer
    end
  end