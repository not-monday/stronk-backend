class RenameWeightToWeights < ActiveRecord::Migration[5.1]
    
    def change
        rename_table :weight, :weights
    end
  end