# Technical Event Management & E-Commerce Web Application

A full-stack web application built using **Flask, SQLite, HTML/CSS, and Python** that supports **multi-role authentication** with separate dashboards for **Admin, Users, and Vendors**.

## Features

### User Module
- User Signup/Login Authentication
- Secure Password Hashing (SHA-256)
- Browse Products
- Add to Cart
- Checkout System
- Order Tracking
- Personal Dashboard

### Admin Module
- Admin Login
- Monitor All Orders
- Approve Orders
- Revenue Dashboard
- Manage Platform Activity

### Vendor Module
- Vendor Login
- Add Products
- Manage Inventory
- Track Sales
- Revenue Analytics Dashboard

## Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS, Jinja2 Templates
- **Authentication:** Session-based Login
- **Security:** SHA-256 Password Encryption

## Database Design
Main tables used:
- Users
- Vendors
- Products
- Cart
- Orders

## Key Learning Outcomes
- Built role-based authentication system
- Designed relational database schema
- Implemented CRUD operations
- Managed session handling
- Developed admin analytics system
- Built end-to-end full-stack application

## Project Structure
```bash
technical-event-project/
│── app.py
│── templates/
│── static/
│── database.db
│── README.md
```

## How to Run
1. Clone repository
```bash
git clone https://github.com/souravjha127/your-repo-name.git
```

2. Install dependencies
```bash
pip install flask
```

3. Run project
```bash
python app.py
```

4. Open browser
```bash
http://127.0.0.1:5000/
```


