import mysql.connector
import csv

def insert_menu_from_csv(csv_path="menu.csv"):
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
            menu_id = int(row["menu_id"]) if row.get("menu_id") else None
            r_id    = int(row["r_id"])     if row.get("r_id")     else None
            f_id    = int(row["f_id"])     if row.get("f_id")     else None
            cuisine = row.get("cuisine")
            price   = float(row["price"]) if row.get("price") not in (None, "") else None

            cur.execute("""
                INSERT IGNORE INTO Menu (menu_id, r_id, f_id, cuisine, price)
                VALUES (%s, %s, %s, %s, %s)
            """, (menu_id, r_id, f_id, cuisine, price))

    db.commit()
    cur.close()
    db.close()

if __name__ == "__main__":
    insert_menu_from_csv("menu.csv")
