# views/courier_view.py
import mysql.connector
from flask import Blueprint, request, jsonify
from helpers.db_helper import get_db_connection # Basit helper'ı import et

courier = Blueprint('courier', __name__)

@courier.route("/", methods=["POST"])
def create_courier():
    """Creates a new courier."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
        
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    password = data.get('password') # güvenlik için hashlenecek
    age = data.get('age')
    gender = data.get('gender')
    marital_status = data.get('maritalStatus')
    experience = data.get('experience', 0)
    r_id = data.get('r_id') 

    # db'ye atmadan önce varlıklarını validate ediyorum
    if not email or not password or not name:
        return jsonify({"error": "Missing required fields: email, password, or name"}), 400

    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500
        
    mycursor = db.cursor()
    try:
        query = (
            "INSERT INTO `Courier` "
            "(`r_id`, `name`, `surname`, `email`, `password`, `age`, `gender`, "
            "`maritalStatus`, `experience`) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        values = (
            r_id, name, surname, email, password, age, gender,
            marital_status, experience
        )
        mycursor.execute(query, values)
        db.commit()
        new_courier_id = mycursor.lastrowid
        
    except mysql.connector.Error as err:
        db.rollback() 
        # bozuk e-posta hatalarını vs yakalar
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        mycursor.close()
        db.close()

    return jsonify({
        "message": "Courier created successfully",
        "c_id": new_courier_id
    }), 201

@courier.route("/", methods=["GET"])
def get_all_couriers():
    """Fetches all couriers."""
    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500
    
    mycursor = db.cursor(dictionary=True) 
    try:
        mycursor.execute("SELECT * FROM Courier")
        couriers = mycursor.fetchall()
        return jsonify(couriers)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        mycursor.close()
        db.close()

@courier.route("/<int:courier_id>", methods=["GET"])
def get_courier(courier_id):
    """Fetches a single courier by c_id."""
    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500
        
    mycursor = db.cursor(dictionary=True)
    try:
        query = "SELECT * FROM Courier WHERE c_id = %s"
        mycursor.execute(query, (courier_id,))
        courier_data = mycursor.fetchone()
        
        if courier_data:
            return jsonify(courier_data)
        else:
            return jsonify({"error": "Courier not found"}), 404
            
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        # Sorgu ne olursa olsun bağlantıyı kapat
        mycursor.close()
        db.close()