import csv
import mysql.connector

# --- CONFIGURATION ---
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password"
DB_NAME = "your_database"
TABLE_NAME = "orders"

# --- CONNECT TO DATABASE ---
db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)
cursor = db.cursor()

# --- OPTIONAL: Create table if not exists ---
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id INT PRIMARY KEY,
    order_date DATE,
    sales_qty INT,
    sales_amount FLOAT,
    currency VARCHAR(10),
    user_id INT,
    r_id FLOAT
);
"""
cursor.execute(create_table_query)

# --- READ AND INSERT DATA FROM CSV ---
with open('../raw_data/orders.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        sql = f"""
        INSERT INTO {TABLE_NAME}
        (id, order_date, sales_qty, sales_amount, currency, user_id, r_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        vals = (
            int(row['Unnamed: 0']),
            row['order_date'],
            int(row['sales_qty']),
            float(row['sales_amount']),
            row['currency'],
            int(row['user_id']),
            float(row['r_id']) if row['r_id'] else None
        )
        cursor.execute(sql, vals)

db.commit()
cursor.close()
db.close()

print("✅ Data inserted successfully!")
