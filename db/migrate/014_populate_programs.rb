class PopulatePrograms < ActiveRecord::Migration[5.1]
    
    def change
        add_column :programs, :name, :string

        sql = "INSERT INTO programs(name, author, description, duration) VALUES"
        names = ["Stronk Training Program", "Stronk Training Program II", "Stronk Training Program III"]
        description = ["An exclusive beginner program on Stronk.",
                        "An exclusive intermediate program on Stronk.",
                        "An exclusive intense program on Stronk."]
        durations = [5, 7, 9]
        authors = [1, 2, 3]
        names.each_with_index do |name, i|
            sql += "('#{name}', '#{authors[i]}', '#{description[i]}', #{durations[i]}), "
        end
        
        sql = sql.slice(0, sql.length - 2) + ";"
        puts sql

        records_array = ActiveRecord::Base.connection.execute(sql)
    end
  end