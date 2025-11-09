# server.py
from flask import Flask, jsonify
import mysql.connector

# viewlerimiz ana dal server'da herkes views folderında kendi endpointlerini yazcak
from views.courier_view import courier
# from views.user_view import user
# from views.restaurant_view import restaurant
# from views.menu_view import menu
# from views.order_view import order

def create_app():
    app = Flask(__name__)
    
    app.config.from_object("config.settings")
    app.config.update(app.config["DB_CONFIG"])


    # --- views baseleri burada tekrar tekrar yazmayalım ve kirletmeyelim burayı diye
    app.register_blueprint(courier, url_prefix='/couriers')
    
    #app.register_blueprint(user, url_prefix='/users')
#
    #app.register_blueprint(restaurant, url_prefix='/restaurants')
    #
    #app.register_blueprint(menu, url_prefix='/menus')
    #
    #app.register_blueprint(order, url_prefix='/orders')


    # --- DB ve API check ---- #
    @app.route("/")
    def home_page():
        try:
            db = mysql.connector.connect(
                host=app.config["DB_HOST"],
                user=app.config["DB_USER"],
                password=app.config["DB_PASSWORD"],
                database=app.config["DB_NAME"]
            )
            db.close()
            return jsonify({"status": "online", "message": "API is running and DB connection is successful."})
        except mysql.connector.Error as err:
            return jsonify({"status": "error", "message": f"API is running, but DB connection failed: {err}"}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 8080)
    
    app.run(
        host="0.0.0.0", 
        port=port, 
        debug=app.config.get("DEBUG", True)
    )