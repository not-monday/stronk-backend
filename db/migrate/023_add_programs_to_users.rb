class AddProgramsToUsers < ActiveRecord::Migration[5.1]

    def change
        sql_statements = ["UPDATE users SET current_program = 1 WHERE id = 1",
                         "UPDATE users SET current_program = 2 WHERE id = 2",
                         "UPDATE users SET current_program = 3 WHERE id = 3",
                         "UPDATE users SET current_program = 2 WHERE id = 4",
                         "UPDATE users SET current_program = 3 WHERE id = 5"]

        sql_statements.each do |sql|
            records_array = ActiveRecord::Base.connection.execute(sql)
        end
    end
end
