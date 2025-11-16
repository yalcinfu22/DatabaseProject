# helpers/db_helper.py
import mysql.connector
from flask import current_app

def get_db_connection(host, user, password, db_name):
    try:
        db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        return db
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None