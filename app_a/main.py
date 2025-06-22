import psycopg2
import random
import uuid
from datetime import datetime
import time


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


def choose_user_id(cur):
    """
    Choose a returning user (30% chance), or create a new one
    """
    if random.random() < 0.3:
        cur.execute("SELECT user_id FROM purchases ORDER BY RANDOM() LIMIT 1;")
        result = cur.fetchone()
        if result:
            return result[0]
    return str(uuid.uuid4())

def simulate_purchase():
    # Connect to the database
    conn = connect_to_db()
    cur = conn.cursor()

    # Fetch available products
    cur.execute("SELECT name, price FROM products;")
    products = cur.fetchall()

    if len(products) < 2:
        print("❌ Not enough products in the database!")
        return

    # Randomly select 2 to 4 products
    num_items = random.randint(2, 4)
    selected = random.sample(products, num_items)

    # Calculate total price and extract product names
    items = [name for name, _ in selected]
    total_amount = sum(price for _, price in selected)

    # Choose supermarket and user
    supermarket_id = random.choice([1, 2, 3])
    user_id = choose_user_id(cur)
    timestamp = datetime.now()

    # Insert the purchase into the 'purchases' table
    try:
        cur.execute("""
            INSERT INTO purchases (supermarket_id, timestamp, user_id, items, total_amount)
            VALUES (%s, %s, %s, %s, %s);
        """, (supermarket_id, timestamp, user_id, items, total_amount))
        conn.commit()
        print("✅ Purchase inserted successfully:")
        print(f"🧍 User ID: {user_id}")
        print(f"🏬 Supermarket ID: SMKT{supermarket_id}")
        print(f"🛒 Items: {items}")
        print(f"💰 Total: {total_amount}")
        print(f"🕒 Timestamp: {timestamp}")
    except Exception as e:
        conn.rollback()
        print("❌ Failed to insert purchase:", e)

    cur.close()
    conn.close()


if __name__ == "__main__":
    while True:
        print("simulate_purchase called")
        simulate_purchase()
        time.sleep(5)  
