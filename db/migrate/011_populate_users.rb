class PopulateUsers < ActiveRecord::Migration[5.1]
    
    def up
        add_column :users, :name, :string
        names = ['Jason', 'Richard', 'Jenny', 'Joe', 'Marissa']
        usernames = ['peakabooweaboo', '13abel', 'max-b-wavy', 'fawix', 'mcohen30']
        emails = ['peakabooweaboo@hotmail.com', '13abel@yahoo.com', 'maxbwavy@gmail.com', 'fawix@outlook.com', 'mcohen30@gmail.com']
        pwd = 'password' 
        sql = "INSERT INTO users(name, username, password, email) VALUES"
        names.each_with_index do |name, i|
            sql += "('#{name}', '#{usernames[i]}', '#{pwd}', '#{emails[i]}'), "
        end
        
        sql = sql.slice(0, sql.length - 2) + ";"
        puts sql

        records_array = ActiveRecord::Base.connection.execute(sql)
    end

    def down
        drop_column :users, :name
    end
  end