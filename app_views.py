from flask import current_app, render_template,request,redirect,url_for
import mysql.connector
from flask import jsonify
import bcrypt
from helpers import db_helper
def home_page():
    cart_count = 0  # or pull from session / DB
    return render_template("main_page.html",
                           active_page="home",
                           cart_count=cart_count)
def user_login():
    return render_template("login.html")
def restaurants():
    return render_template("restaurants.html")
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
     salary = request.form.get("salary")
     status = request.form.get("martial_status")
     occupation = request.form.get("occupation")
     age = request.form.get("age")
     password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
     db = db_helper.get_db_connection("localhost", "root", "123654","term_project")
     query = (
                    "INSERT INTO `user` "
                    "(name, email, password, Age, Gender, Marital_Status, Occupation, Monthly_Income, city, address) "
                    "VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
     values = (first_name + " " + last_name, email, password_hash, age, gender,
                          status, occupation, salary, city,
                          address)
     mycursor = db.cursor()
     mycursor.execute(query, values)
     db.commit()
     return redirect(url_for("home_page"))
     