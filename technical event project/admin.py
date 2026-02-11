import pandas as pd
import sqlite3

def create_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        product_name TEXT,
        price REAL,
        quantity INTEGER,
        vendor_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        product_id TEXT,
        quantity INTEGER,
        status TEXT DEFAULT 'Pending'
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart (
        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        product_id TEXT,
        quantity INTEGER
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendors (
        vendor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)


    conn.commit()
    conn.close()
    create_user_table()

def create_user_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()

def admin_menu():
    create_table()

    while True:
        print("\n===== Admin Panel =====")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Back")
        print("6. View All Orders")
        print("7. Update Order Status")


        choice = input("Enter your choice: ")

        if choice == "1":
            add_product()

        elif choice == "2":
            view_products()

        elif choice == "3":
            update_product()
        elif choice== "4":
            delete_product()
        elif choice =="5":
            break
        elif choice == "6":
            view_all_orders()
        elif choice == "7":
            update_order_status()

def add_product():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    product_id = input("Enter Product ID: ")
    product_name = input("Enter Product Name: ")
    price = float(input("Enter Price: "))
    quantity = int(input("Enter Quantity: "))

    try:
        cursor.execute("INSERT INTO products VALUES (?, ?, ?, ?)",
                       (product_id, product_name, price, quantity))
        conn.commit()
        print("✅ Product Added Successfully!")
    except:
        print("❌ Product ID already exists!")

    conn.close()


def view_products():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()

    print("\n===== Product List =====")
    for row in rows:
        print(row)

    conn.close()

def delete_product():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    product_id = input("Enter Product ID to delete: ")

    cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
    conn.commit()

    if cursor.rowcount > 0:
        print("✅ Product Deleted Successfully!")
    else:
        print("❌ Product Not Found!")

    conn.close()
    
def update_product():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    product_id = input("Enter Product ID to update: ")
    new_price = float(input("Enter New Price: "))
    new_quantity = int(input("Enter New Quantity: "))

    cursor.execute("""
        UPDATE products
        SET price = ?, quantity = ?
        WHERE product_id = ?
    """, (new_price, new_quantity, product_id))

    conn.commit()

    if cursor.rowcount > 0:
        print("✅ Product Updated Successfully!")
    else:
        print("❌ Product Not Found!")

    conn.close()
def view_all_orders():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT orders.order_id, orders.username, products.product_name, orders.quantity, products.price
        FROM orders
        JOIN products ON orders.product_id = products.product_id
    """)

    rows = cursor.fetchall()

    print("\n===== All Orders =====")
    total_revenue = 0

    for row in rows:
        order_id, username, product_name, quantity, price = row
        revenue = quantity * price
        total_revenue += revenue

        print(f"OrderID: {order_id}, User: {username}, Product: {product_name}, Qty: {quantity}, Revenue: {revenue}")

    print(f"\n💰 Total Revenue: {total_revenue}")

    conn.close()
def update_order_status():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    order_id = input("Enter Order ID: ")
    print("Choose Status:")
    print("1. Approved")
    print("2. Shipped")
    print("3. Completed")
    print("4. Cancelled")

    choice = input("Enter choice: ")

    status_dict = {
        "1": "Approved",
        "2": "Shipped",
        "3": "Completed",
        "4": "Cancelled"
    }

    if choice in status_dict:
        new_status = status_dict[choice]
        cursor.execute("UPDATE orders SET status=? WHERE order_id=?",
                       (new_status, order_id))
        conn.commit()
        print("✅ Status Updated!")
    else:
        print("❌ Invalid choice")

    conn.close()
def view_all_users():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM users")
    rows = cursor.fetchall()

    print("\n===== All Users =====")
    for row in rows:
        print(row[0])

    conn.close()
def revenue_summary():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT products.price, orders.quantity
        FROM orders
        JOIN products ON orders.product_id = products.product_id
        WHERE status='Completed'
    """)

    rows = cursor.fetchall()

    total = 0
    for price, quantity in rows:
        total += price * quantity

    print(f"\n💰 Total Completed Revenue: {total}")

    conn.close()
