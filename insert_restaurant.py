import mysql.connector
import csv

def insert_restaurant_from_csv(csv_path="restaurant.csv"):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="term_project"
    )
    cur = db.cursor()

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            id = int(row["menu_id"]) if row.get("menu_id") else None
            name = row.get("name")
            city = row.get("city")
            rating = row.get("rating")
            rating_count = row.get("rating_count")
            cost = row.get("cost")
            cuisine = row.get("cuisine")
            lic_no = row.get("lic_no")
            link = row.get("link")
            address = row.get("address")
            
            sql = """
                INSERT IGNORE INTO Restaurant (
                    id, name, city, rating, rating_count, 
                    cost, cuisine, lic_no, link, address, menu_file
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            val = (
                id, name, city, rating, rating_count,
                cost, cuisine, lic_no, link, address
            )
                
            cur.execute(sql, val)

    db.commit()
    cur.close()
    db.close()

if __name__ == "__main__":
    insert_restaurant_from_csv("raw_data/restaurant.csv")
