import pandas as pd
import mysql.connector
from datetime import datetime
import logging
import re

# ---------------- LOGGING SETUP ----------------
logging.basicConfig(
    filename="data_quality_report.txt",
    filemode="w",
    level=logging.INFO,
    format="%(message)s"
)

# ---------------- DB CONNECTION ----------------
conn = mysql.connector.connect(
    host="localhost",
    user="flexi_user",
    password="flexi_pass",
    database="fleximart"
)
cursor = conn.cursor()

# ---------------- UTILS ----------------
def standardize_phone(phone):
    if pd.isna(phone):
        return None
    digits = re.sub(r"\D", "", str(phone))
    return f"+91-{digits[-10:]}" if len(digits) >= 10 else None

def standardize_category(cat):
    if pd.isna(cat):
        return None
    return cat.strip().title()

def parse_date(date_str):
    if pd.isna(date_str):
        return None
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(str(date_str), fmt).date()
        except:
            continue
    return None

# ---------------- EXTRACT ----------------
try:
    customers = pd.read_csv("data/customers_raw.csv")
    products = pd.read_csv("data/products_raw.csv")
    sales = pd.read_csv("data/sales_raw.csv")
except FileNotFoundError as e:
    logging.error(f"File not found: {e}")
    cursor.close()
    conn.close()
    raise

# ---------------- TRANSFORM ----------------
orig_counts = {
    "customers": len(customers),
    "products": len(products),
    "sales": len(sales)
}

# Store original IDs before cleaning
customers['original_customer_id'] = customers['customer_id']
products['original_product_id'] = products['product_id']

# Drop duplicates
customers = customers.drop_duplicates(subset=["email"], keep='first')
products = products.drop_duplicates(subset=["product_name"], keep='first')
sales = sales.drop_duplicates(keep='first')

# Clean customers
customers = customers.dropna(subset=["email"])
customers["phone"] = customers["phone"].apply(standardize_phone)
customers["registration_date"] = customers["registration_date"].apply(parse_date)

# Clean products
products["price"] = products["price"].fillna(products["price"].mean())
products["category"] = products["category"].apply(standardize_category)
products["stock_quantity"] = products["stock_quantity"].fillna(0)

# Clean sales
sales["transaction_date"] = sales["transaction_date"].apply(parse_date)
sales = sales.rename(columns={"transaction_date": "order_date"})
sales = sales.dropna(subset=["customer_id", "product_id"])

# ---------------- LOAD ----------------
try:
    # ---- LOAD CUSTOMERS ----
    customer_id_map = {}  # Maps original customer_id (C001) to new DB ID
    for _, row in customers.iterrows():
        cursor.execute("""
            INSERT INTO customers (email, phone, registration_date)
            VALUES (%s, %s, %s)
        """, (
            row["email"],
            row["phone"],
            row["registration_date"]
        ))
        customer_id_map[row["original_customer_id"]] = cursor.lastrowid

    print(f"Loaded {len(customers)} customers")

    # ---- LOAD PRODUCTS ----
    product_id_map = {}  # Maps original product_id (P001) to new DB ID
    for _, row in products.iterrows():
        cursor.execute("""
            INSERT INTO products (product_name, category, price, stock_quantity)
            VALUES (%s, %s, %s, %s)
        """, (
            row["product_name"],
            row["category"],
            float(row["price"]),
            int(row["stock_quantity"])
        ))
        product_id_map[row["original_product_id"]] = cursor.lastrowid

    print(f"Loaded {len(products)} products")

    # ---- LOAD ORDERS & ORDER ITEMS ----
    orders_loaded = 0
    orders_skipped = 0
    
    for _, row in sales.iterrows():
        # Get mapped IDs
        customer_db_id = customer_id_map.get(row["customer_id"])
        product_db_id = product_id_map.get(row["product_id"])
        
        # Skip if IDs don't exist in our mappings
        if customer_db_id is None or product_db_id is None:
            orders_skipped += 1
            continue
        
        # Insert order
        cursor.execute("""
            INSERT INTO orders (customer_id, order_date)
            VALUES (%s, %s)
        """, (
            customer_db_id,
            row["order_date"]
        ))
        order_id = cursor.lastrowid

        # Insert order item
        cursor.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            order_id,
            product_db_id,
            int(row["quantity"]),
            float(row["unit_price"]),
            float(row["quantity"] * row["unit_price"])
        ))
        
        orders_loaded += 1

    print(f"Loaded {orders_loaded} orders ({orders_skipped} skipped due to missing references)")

    # Commit all changes
    conn.commit()

    # ---------------- REPORT ----------------
    logging.info("=" * 50)
    logging.info("DATA QUALITY REPORT")
    logging.info("=" * 50)
    logging.info(f"Customers processed: {orig_counts['customers']} → {len(customers)}")
    logging.info(f"Products processed: {orig_counts['products']} → {len(products)}")
    logging.info(f"Sales processed: {orig_counts['sales']} → {orders_loaded} (skipped: {orders_skipped})")
    logging.info("=" * 50)
    logging.info("ETL Completed Successfully")
    
    print("\n" + "=" * 50)
    print("ETL process completed successfully!")
    print("=" * 50)
    print(f"Check 'data_quality_report.txt' for details")

except mysql.connector.Error as err:
    logging.error(f"Database error: {err}")
    conn.rollback()
    print(f"Database Error: {err}")
    raise

except Exception as e:
    logging.error(f"Unexpected error: {e}")
    conn.rollback()
    print(f"Error: {e}")
    raise

finally:
    # Close connections
    cursor.close()
    conn.close()