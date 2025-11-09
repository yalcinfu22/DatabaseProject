from flask import current_app, render_template,request,redirect,url_for
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
def  user_submit_signup_form():
     first_name = request.form.get("first_name")
     last_name = request.form.get("last_name")
     password = request.form.get("password")
     address = request.form.get("address")
     city = request.form.get("city")
     email = request.form.get("email")
     gender = request.form.get("gender")
     print(gender)
     return redirect(url_for("home_page"))
     