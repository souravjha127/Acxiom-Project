from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = "secretkey"

# 🔥 SHARED DATABASE
DATABASE = "C:/technical event project/database.db"


# ================= HOME =================
@app.route("/")
def home():
    return render_template("index.html")


# ================= SIGNUP =================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users VALUES (?, ?)", (username, hashed_password))
            conn.commit()
        except:
            return "Username already exists"

        conn.close()
        return redirect(url_for("login"))

    return render_template("signup.html")


# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                       (username, hashed_password))

        user = cursor.fetchone()
        conn.close()

        if user:
            session["username"] = username

            if username == "admin":
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials"

    return render_template("login.html")


# ================= USER DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", username=session["username"])


# ================= PRODUCTS =================
@app.route("/products")
def products():
    if "username" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT product_id, product_name, price, quantity FROM products")
    products = cursor.fetchall()

    conn.close()

    return render_template("products.html", products=products)


# ================= ADD TO CART =================
@app.route("/add_to_cart/<product_id>")
def add_to_cart(product_id):
    if "username" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO cart (username, product_id, quantity) VALUES (?, ?, ?)",
                   (session["username"], product_id, 1))

    conn.commit()
    conn.close()

    return redirect(url_for("products"))


# ================= CART =================
@app.route("/cart")
def cart():
    if "username" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT products.product_name, cart.quantity
        FROM cart
        JOIN products ON cart.product_id = products.product_id
        WHERE cart.username=?
    """, (session["username"],))

    items = cursor.fetchall()
    conn.close()

    return render_template("cart.html", items=items)


# ================= CHECKOUT =================
@app.route("/checkout")
def checkout():
    if "username" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT product_id, quantity FROM cart WHERE username=?", (session["username"],))
    items = cursor.fetchall()

    for product_id, quantity in items:
        cursor.execute("SELECT quantity FROM products WHERE product_id=?", (product_id,))
        stock = cursor.fetchone()

        if stock and stock[0] >= quantity:
            new_quantity = stock[0] - quantity

            cursor.execute("UPDATE products SET quantity=? WHERE product_id=?",
                           (new_quantity, product_id))

            cursor.execute("""
                INSERT INTO orders (username, product_id, quantity, status)
                VALUES (?, ?, ?, ?)
            """, (session["username"], product_id, quantity, "Pending"))

    cursor.execute("DELETE FROM cart WHERE username=?", (session["username"],))

    conn.commit()
    conn.close()

    return redirect(url_for("orders"))


# ================= USER ORDERS =================
@app.route("/orders")
def orders():
    if "username" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT order_id, product_id, quantity, status
        FROM orders
        WHERE username=?
    """, (session["username"],))

    orders = cursor.fetchall()
    conn.close()

    return render_template("orders.html", orders=orders)


# ================= ADMIN =================
@app.route("/admin")
def admin_dashboard():
    if "username" not in session or session["username"] != "admin":
        return redirect(url_for("login"))

    return render_template("admin_dashboard.html")


@app.route("/admin_orders")
def admin_orders():
    if "username" not in session or session["username"] != "admin":
        return redirect(url_for("login"))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT order_id, username, product_id, quantity, status FROM orders")
    orders = cursor.fetchall()

    conn.close()
    return render_template("admin_orders.html", orders=orders)


@app.route("/update_status/<int:order_id>")
def update_status(order_id):
    if "username" not in session or session["username"] != "admin":
        return redirect(url_for("login"))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("UPDATE orders SET status='Approved' WHERE order_id=?", (order_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("admin_orders"))


@app.route("/revenue")
def revenue():
    if "username" not in session or session["username"] != "admin":
        return redirect(url_for("login"))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT products.price, orders.quantity
        FROM orders
        JOIN products ON orders.product_id = products.product_id
        WHERE orders.status='Approved'
    """)

    rows = cursor.fetchall()
    total = sum(price * quantity for price, quantity in rows)

    conn.close()
    return render_template("revenue.html", total=total)


# ================= VENDOR =================
@app.route("/vendor_login", methods=["GET", "POST"])
def vendor_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("SELECT vendor_id FROM vendors WHERE username=? AND password=?",
                       (username, hashed_password))

        vendor = cursor.fetchone()
        conn.close()

        if vendor:
            session["vendor_id"] = vendor[0]
            session["vendor_name"] = username
            return redirect(url_for("vendor_dashboard"))
        else:
            return "Invalid Vendor Credentials"

    return render_template("vendor_login.html")


@app.route("/vendor_dashboard")
def vendor_dashboard():
    if "vendor_id" not in session:
        return redirect(url_for("vendor_login"))

    return render_template("vendor_dashboard.html",
                           vendor=session["vendor_name"])


@app.route("/vendor_products")
def vendor_products():
    if "vendor_id" not in session:
        return redirect(url_for("vendor_login"))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT product_id, product_name, price, quantity
        FROM products
        WHERE vendor_id=?
    """, (session["vendor_id"],))

    products = cursor.fetchall()
    conn.close()

    return render_template("vendor_products.html", products=products)


@app.route("/vendor_add_product", methods=["GET", "POST"])
def vendor_add_product():
    if "vendor_id" not in session:
        return redirect(url_for("vendor_login"))

    if request.method == "POST":
        product_id = request.form["product_id"]
        name = request.form["name"]
        price = float(request.form["price"])
        quantity = int(request.form["quantity"])

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO products (product_id, product_name, price, quantity, vendor_id)
            VALUES (?, ?, ?, ?, ?)
        """, (product_id, name, price, quantity, session["vendor_id"]))

        conn.commit()
        conn.close()

        return redirect(url_for("vendor_products"))

    return render_template("vendor_add_product.html")


@app.route("/vendor_revenue")
def vendor_revenue():
    if "vendor_id" not in session:
        return redirect(url_for("vendor_login"))

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT products.price, orders.quantity
        FROM orders
        JOIN products ON orders.product_id = products.product_id
        WHERE products.vendor_id=? AND orders.status='Approved'
    """, (session["vendor_id"],))

    rows = cursor.fetchall()
    total = sum(price * quantity for price, quantity in rows)

    conn.close()
    return render_template("vendor_revenue.html", total=total)


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
