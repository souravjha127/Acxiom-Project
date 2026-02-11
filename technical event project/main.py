import pandas as pd
import admin
import user
import vendor

admin.create_table()


def main_menu():
    print("===== Technical Event Management System =====")
    print("1. Admin Login")
    print("2. User Login")
    print("3. Vendor Login")
    print("4. Exit")

    choice = input("Enter your choice: ")
    return choice

while True:
    choice = main_menu()

    if choice == "1":
        admin.admin_menu()
    elif choice == "2":
        user.user_menu()
    elif choice == "3":
        vendor.vendor_menu()

    elif choice == "4":
        print("Exiting Program...")
        break
    else:
        print("Invalid Choice")
