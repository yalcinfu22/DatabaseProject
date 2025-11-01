import mysql.connector
import csv
## this file aim to insert data from our csv to database tables
def insert_user():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database = "term_project"
    )
    mycursor = mydb.cursor()
    with open("users.csv") as file_obj:
        read_csv = csv.reader(file_obj)
        i = 0
        for row in read_csv:
            if i == 1 :
                id, name, email, password, age, gender, marital_status, occupation, monthly_income  = int(row[1]), row[2], row[3], row[4], int(row[5]), row[6], row[7], row[8], row[9]
                address, city = "", ""
                query = (
            "INSERT INTO `user` "
            "(user_id, user_name, email, password, age, gender, martial_status, occuption, monthly_income, city, address) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
                values = (id, name, email, password, age, gender,
        marital_status, occupation, monthly_income, city ,address
    )
                mycursor.execute(query, values)
            i = 1
        mydb.commit()

