import sqlite3
import hashlib

def vendor_menu():
    while True:
        print("\n===== Vendor Panel =====")
        print("1. Signup")
        print("2. Login")
        print("3. Back")

        choice = input("Enter choice: ")

        if choice == "1":
            signup()
        elif choice == "2":
            login()
        elif choice == "3":
            break
        else:
            print("Invalid choice")


def signup():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        cursor.execute("INSERT INTO vendors (username, password) VALUES (?, ?)",
                       (username, hashed_password))
        conn.commit()
        print("✅ Vendor Signup Successful!")
    except:
        print("❌ Username already exists!")

    conn.close()


def login():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute("SELECT vendor_id FROM vendors WHERE username=? AND password=?",
                   (username, hashed_password))

    vendor = cursor.fetchone()

    if vendor:
        print("✅ Login Successful!")
        vendor_dashboard(vendor[0])
    else:
        print("❌ Invalid Credentials!")

    conn.close()


def vendor_dashboard(vendor_id):
    while True:
        print("\n===== Vendor Dashboard =====")
        print("1. Add Product")
        print("2. View My Products")
        print("3. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            add_product(vendor_id)
        elif choice == "2":
            view_my_products(vendor_id)
        elif choice == "3":
            break
        else:
            print("Invalid choice")


def add_product(vendor_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    product_id = input("Enter Product ID: ")
    name = input("Enter Product Name: ")
    price = float(input("Enter Price: "))
    quantity = int(input("Enter Quantity: "))

    try:
        cursor.execute("""
            INSERT INTO products (product_id, product_name, price, quantity, vendor_id)
            VALUES (?, ?, ?, ?, ?)
        """, (product_id, name, price, quantity, vendor_id))

        conn.commit()
        print("✅ Product Added Successfully!")
    except:
        print("❌ Product ID already exists!")

    conn.close()


def view_my_products(vendor_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE vendor_id=?", (vendor_id,))
    rows = cursor.fetchall()

    print("\n===== My Products =====")
    for row in rows:
        print(row)

    conn.close()
