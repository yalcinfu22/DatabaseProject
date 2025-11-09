import mysql.connector
from flask import Blueprint, request, jsonify
from helpers.db_helper import get_db_connection

menu = Blueprint("menu", __name__)

@menu.route("/", methods=["POST"])
def create_menu_item():
    """
    Body örneği:
    {
      "menu_id": "mn0",
      "r_id": 567335,
      "f_id": "fd0",
      "cuisine": "Beverages,Pizzas",
      "price": 40.0
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    menu_id = data.get("menu_id")
    r_id    = data.get("r_id")
    f_id    = data.get("f_id")
    cuisine = data.get("cuisine")
    price   = data.get("price")

    if menu_id is None or r_id is None or f_id is None or price is None:
        return jsonify({
            "error": "Missing fields: menu_id, r_id, f_id, price"
        }), 400

    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    cur = db.cursor()
    try:
        cur.execute(
            """
            INSERT INTO Menu (menu_id, r_id, f_id, cuisine, price)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (menu_id, r_id, f_id, cuisine, price),
        )
        db.commit()
        new_id = cur.lastrowid
    except mysql.connector.Error as err:
        db.rollback()
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        cur.close()
        db.close()

    return jsonify({
        "message": "Menu item created successfully",
        "m_id": new_id
    }), 201


@menu.route("/", methods=["GET"])
def get_all_menu_items():
    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    cur = db.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM Menu")
        rows = cur.fetchall()
        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        cur.close()
        db.close()


@menu.route("/<int:m_id>", methods=["GET"])
def get_menu_item(m_id):
    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    cur = db.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM Menu WHERE m_id = %s", (m_id,))
        row = cur.fetchone()
        if row:
            return jsonify(row)
        return jsonify({"error": "Menu item not found"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        cur.close()
        db.close()


@menu.route("/by-restaurant/<int:r_id>", methods=["GET"])
def get_menu_by_restaurant(r_id):
    db = get_db_connection()
    if not db:
        return jsonify({"error": "Database connection failed"}), 500

    cur = db.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM Menu WHERE r_id = %s", (r_id,))
        rows = cur.fetchall()
        return jsonify(rows)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Database error: {err}"}), 500
    finally:
        cur.close()
        db.close()