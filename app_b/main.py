import psycopg2
from collections import Counter
import psycopg2
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


def get_unique_buyers(cur):
    cur.execute("SELECT COUNT(DISTINCT user_id) FROM purchases;")
    result = cur.fetchone()
    return result[0] if result else 0

def get_loyal_customers(cur, min_purchases=3):
    cur.execute("""
        SELECT user_id
        FROM purchases
        GROUP BY user_id
        HAVING COUNT(*) >= %s;
    """, (min_purchases,))
    results = cur.fetchall()
    return [row[0] for row in results]

def get_top_selling_products(cur, top_n=3):
    # Aggregate all items from purchases into one big list
    cur.execute("SELECT items FROM purchases;")
    all_items = []
    for row in cur.fetchall():
        all_items.extend(row[0])  # row[0] is an array of product names

    # Count frequency of each product
    counter = Counter(all_items)
    if not counter:
        return []

    # Find the Nth highest count (to include ties)
    counts = sorted(set(counter.values()), reverse=True)
    threshold = counts[top_n-1] if len(counts) >= top_n else counts[-1]

    # Get all products with count >= threshold
    top_products = [(prod, cnt) for prod, cnt in counter.items() if cnt >= threshold]

    # Sort by frequency descending, then product name ascending
    top_products.sort(key=lambda x: (-x[1], x[0]))

    return top_products

def main():
    conn = connect_to_db()
    cur = conn.cursor()

    print("🛒 Supermarket Owner Dashboard\n")

    unique_buyers = get_unique_buyers(cur)
    print(f"1️⃣ Unique buyers in network: {unique_buyers}")

    loyal_customers = get_loyal_customers(cur)
    print(f"2️⃣ Loyal customers (≥3 purchases):")
    for user in loyal_customers:
        print(f" - {user}")

    top_products = get_top_selling_products(cur, top_n=3)
    print(f"3️⃣ Top selling products (including ties):")
    for prod, cnt in top_products:
        print(f" - {prod}: {cnt} sold")

    cur.close()
    conn.close()

if __name__ == "__main__":
    while True:
        main()
        print("⏳ Waiting before next dashboard refresh...")
        time.sleep(45)  
