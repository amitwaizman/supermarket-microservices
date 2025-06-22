import psycopg2
import csv
import time
from datetime import datetime

def connect_to_db(retries=10, delay=3):
    for attempt in range(retries):
        try:
            conn = psycopg2.connect(
                host="db",
                database="supermarket",
                user="postgres",
                password="password"
            )
            print(f"✅ Connected to DB on attempt {attempt+1}")
            return conn
        except psycopg2.OperationalError as e:
            print(f"⏳ Attempt {attempt+1}/{retries} - DB not ready yet: {e}")
            time.sleep(delay)
    print("❌ Could not connect to the database after multiple attempts.")
    exit(1)

conn = connect_to_db()
cur = conn.cursor()

# --- Loading products ---
print("🔄 Importing products from products_list.csv...")
with open('products_list.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f) 
    for row in reader:
        try:
            name = row['product_name'].strip()
            price = float(row['unit_price'].strip())
            cur.execute("INSERT INTO products (name, price) VALUES (%s, %s);", (name, price))
            print(f"✅ Inserted product: {name} at {price}")
        except Exception as e:
            print(f"❌ Failed to insert product {row}: {e}")

# --- Loading purchases ---
print("\n🔄 Importing purchases from purchases.csv...")
with open('purchases.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            supermarket_id = int(row['supermarket_id'].replace('SMKT', ''))
            timestamp = datetime.fromisoformat(row['timestamp'].strip())
            user_id = row['user_id'].strip()
            items_list_raw = row['items_list'].strip()
            items = [item.strip() for item in items_list_raw.split(',')]
            total_amount = float(row['total_amount'].strip())

            cur.execute("""
                INSERT INTO purchases (supermarket_id, timestamp, user_id, items, total_amount)
                VALUES (%s, %s, %s, %s, %s);
            """, (supermarket_id, timestamp, user_id, items, total_amount))
            print(f"✅ Inserted purchase for user {user_id}: {items} - {total_amount}")
        except Exception as e:
            print(f"❌ Failed to insert purchase {row}: {e}")
            conn.rollback()

conn.commit()
cur.close()
conn.close()
print("\n🎉 Data loading complete!")
