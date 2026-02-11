import sqlite3
import hashlib

def user_menu():
    while True:
        print("\n===== User Panel =====")
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
        cursor.execute("INSERT INTO users VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("✅ Signup Successful!")
    except:
        print("❌ Username already exists!")

    conn.close()



def login():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                   (username, hashed_password))

    user = cursor.fetchone()

    if user:
        print("✅ Login Successful!")
        user_dashboard(username)
    else:
        print("❌ Invalid Credentials!")

    conn.close()

def user_dashboard(username):
    while True:
        print(f"\n===== Welcome {username} =====")
        print("1. View Products")
        print("2. Add to Cart")
        print("3. View Cart")
        print("4. Checkout")
        print("5. View My Orders")
        print("6. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            view_products()

        elif choice == "2":
            add_to_cart(username)

        elif choice == "3":
            view_cart(username)

        elif choice == "4":
            checkout(username)

        elif choice == "5":
            view_orders(username)

        elif choice == "6":
            break

        else:
            print("Invalid choice")

def view_products():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()

    print("\n===== Available Products =====")
    for row in rows:
        print(row)

    conn.close()
def buy_product(username):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    product_id = input("Enter Product ID to buy: ")
    quantity = int(input("Enter quantity: "))

    cursor.execute("SELECT quantity FROM products WHERE product_id=?", (product_id,))
    result = cursor.fetchone()

    if result:
        available_quantity = result[0]

        if available_quantity >= quantity:
            new_quantity = available_quantity - quantity

            cursor.execute("UPDATE products SET quantity=? WHERE product_id=?",
                           (new_quantity, product_id))
            cursor.execute("INSERT INTO orders (username, product_id, quantity) VALUES (?, ?, ?)",
                           (username, product_id, quantity))

            conn.commit()

            print("✅ Purchase Successful!")
        else:
            print("❌ Not enough stock!")
    else:
        print("❌ Product not found!")

    conn.close()
def view_orders(username):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT order_id, product_id, quantity, status
        FROM orders
        WHERE username=?
    """, (username,))

    rows = cursor.fetchall()

    print("\n===== My Orders =====")

    if not rows:
        print("No orders found.")
    else:
        for row in rows:
            order_id, product_id, quantity, status = row
            print(f"Order ID: {order_id}")
            print(f"Product ID: {product_id}")
            print(f"Quantity: {quantity}")
            print(f"Status: {status}")
            print("----------------------")

    conn.close()

def add_to_cart(username):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    product_id = input("Enter Product ID: ")
    quantity = int(input("Enter Quantity: "))

    cursor.execute("INSERT INTO cart (username, product_id, quantity) VALUES (?, ?, ?)",
                   (username, product_id, quantity))

    conn.commit()
    print("✅ Added to Cart!")
    conn.close()
def view_cart(username):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT products.product_name, cart.quantity
        FROM cart
        JOIN products ON cart.product_id = products.product_id
        WHERE cart.username=?
    """, (username,))

    rows = cursor.fetchall()

    print("\n===== My Cart =====")

    if not rows:
        print("Cart is empty.")
    else:
        for row in rows:
            print(f"Product: {row[0]}, Quantity: {row[1]}")

    conn.close()
def checkout(username):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT product_id, quantity FROM cart WHERE username=?", (username,))
    cart_items = cursor.fetchall()

    if not cart_items:
        print("❌ Cart is empty.")
        conn.close()
        return

    for product_id, quantity in cart_items:
       
        cursor.execute("SELECT quantity FROM products WHERE product_id=?", (product_id,))
        result = cursor.fetchone()

        if result and result[0] >= quantity:
            new_quantity = result[0] - quantity

        
            cursor.execute("UPDATE products SET quantity=? WHERE product_id=?",
                           (new_quantity, product_id))

            cursor.execute("INSERT INTO orders (username, product_id, quantity, status) VALUES (?, ?, ?, ?)",
               (username, product_id, quantity, "Pending"))

        else:
            print(f"❌ Not enough stock for {product_id}")
            conn.close()
            return

    cursor.execute("DELETE FROM cart WHERE username=?", (username,))

    conn.commit()
    conn.close()

    print("✅ Checkout Successful!")
