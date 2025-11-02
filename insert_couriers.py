import mysql.connector
import csv

def insert_couriers():
    
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="term_project"
    )
    
    mycursor = mydb.cursor()
    
    with open("couriers.csv", mode='r') as file_obj:
        read_csv = csv.reader(file_obj)
        
        i = 0 
        for row in read_csv:
            if i == 1:

                r_id = int(row[0]) if row[0] else None 

                name = row[1]
                surname = row[2]
                email = row[3]
                password = row[4]
                age = int(row[5])
                gender = row[6]
                marital_status = row[7]
                experience = int(row[8])
                rating = float(row[9])
                rating_count = int(row[10])
                task_count = int(row[11])
                
                query = (
                    "INSERT INTO `Courier` "
                    "(`r_id`, `name`, `surname`, `email`, `password`, `Age`, `Gender`, "
                    "`MaritalStatus`, `experience`, `rating`, `ratingCount`, `taskCount`) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                )
                
                # values to be inserted to the db
                values = (
                    r_id, name, surname, email, password, age, gender,
                    marital_status, experience, rating, rating_count, task_count
                )
                
                # use the query with the values
                mycursor.execute(query, values)
            
            # flag to skip the header line
            i = 1 
            
    # apply all changes
    mydb.commit()
