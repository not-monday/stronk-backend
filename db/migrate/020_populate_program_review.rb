class PopulateProgramReview < ActiveRecord::Migration[5.1]
    
    def change
        sql = "INSERT INTO program_reviews(program_id, author, rating, review) VALUES"
        
        reviews = ["Great program!", "My favourite!", "I can definitely see the results.", "Would recommend to a friend!", "Excellent!"]
        (1..5).each do |i|
            sql += "('#{rand(1..3)}', '#{i}', '#{rand(4..5)}', '#{reviews[i]}'), "
        end
        
        sql = sql.slice(0, sql.length - 2) + ";"
        puts sql

        records_array = ActiveRecord::Base.connection.execute(sql)
    end
end