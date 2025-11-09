from flask import current_app, render_template
import mysql.connector
from flask import jsonify
def home_page():
        try:
            db = mysql.connector.connect(
                host="",
                user="",
                password="",
                database=""
            )
            db.close()
            return jsonify({"status": "online", "message": "API is running and DB connection is successful."})
        except mysql.connector.Error as err:
            return jsonify({"status": "error", "message": f"API is running, but DB connection failed: {err}"}), 500
def user_signup():
    return render_template("/user_agent.html")