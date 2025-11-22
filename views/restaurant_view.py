from flask import Blueprint, render_template, request, redirect, url_for, session
import bcrypt
from helpers import db_helper

restaurant = Blueprint('restaurant', __name__)

@restaurant.route('/login')
def restaurant_login():
    """Restaurant manager login page"""
    return render_template('restaurant_login.html')

@restaurant.route('/submit_login', methods=['POST'])
def restaurant_submit_login():
    """Handle restaurant manager login"""
    email = request.form.get("email")
    password = request.form.get("password")
    
    if not email or not password:
        return "Email and password are required", 400
    
    # Database lookup
    db = db_helper.get_db_connection("localhost", "root", "123654", "term_project")
    cursor = db.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM Restaurant WHERE email = %s", (email,))
        restaurant_data = cursor.fetchone()
        
        if restaurant_data and bcrypt.checkpw(password.encode("utf-8"), restaurant_data['password'].encode("utf-8")):
            # Login successful
            session['user_id'] = restaurant_data['r_id']
            session['user_name'] = restaurant_data['restaurant_name']
            session['user_type'] = 'restaurant'
            return redirect(url_for('home_page.home_page'))
        else:
            return "Invalid email or password", 401
    except Exception as e:
        print(f"Login error: {e}")
        return f"An error occurred: {e}", 500
    finally:
        cursor.close()
        db.close()

@restaurant.route('/logout')
def restaurant_logout():
    """Restaurant logout"""
    session.clear()
    return redirect(url_for('home_page.home_page'))

@restaurant.route('/signup')
def restaurant_signup():
    """Restaurant manager signup page"""
    return render_template('restaurant_signup.html')

@restaurant.route('/submit_signup', methods=['POST'])
def restaurant_submit_signup():
    """Handle restaurant signup form submission"""
    restaurant_name = request.form.get("restaurant_name")
    manager_name = request.form.get("manager_name")
    email = request.form.get("email")
    password = request.form.get("password")
    phone = request.form.get("phone")
    city = request.form.get("city")
    address = request.form.get("address")
    cuisine = request.form.get("cuisine")
    restaurant_key = request.form.get("restaurant_key")
    description = request.form.get("description", "")

    if not password:
        return "Password required", 400

    # Hash password
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Database Insert
    db = db_helper.get_db_connection("localhost", "root", "123654", "term_project")
    cursor = db.cursor()
    
    query = """
        INSERT INTO Restaurant 
        (restaurant_name, manager_name, email, password, phone, city, address, cuisine, description) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    values = (restaurant_name, manager_name, email, password_hash, phone, city, address, cuisine, description)
    
    try:
        cursor.execute(query, values)
        db.commit()
        print("Restaurant Registered Successfully")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        return f"Registration failed: {e}", 500
    finally:
        cursor.close()
        db.close()

    return redirect(url_for("home_page.home_page"))