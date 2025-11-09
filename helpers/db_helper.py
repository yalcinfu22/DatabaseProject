# helpers/db_helper.py
import mysql.connector
from flask import current_app

def get_db_connection():
    try:
        db = mysql.connector.connect(
            host=current_app.config["DB_HOST"],
            user=current_app.config["DB_USER"],
            password=current_app.config["DB_PASSWORD"],
            database=current_app.config["DB_NAME"]
        )
        return db
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None