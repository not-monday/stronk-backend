class PopulateWeightRelation < ActiveRecord::Migration[5.1]
    
    def change
        add_column :weight, :name, :string

        sql = "INSERT INTO weight(date, weight, user_id) VALUES"
        dates = ["2019-10-18", "2019-10-25", "2019-11-02",
                 "2019-09-15", "2019-09-22", "2019-09-29"]
        user_ids = [1, 2, 3, 4, 5]
        weights = [90, 95, 100, 97, 105, 112]
        dates.each_with_index do |date, i|
            sql += "('#{date}', '#{weights[i] + user_ids[i]}', #{user_ids[i]}), "
        end
        
        sql = sql.slice(0, sql.length - 2) + ";"
        puts sql

        records_array = ActiveRecord::Base.connection.execute(sql)
    end
  end