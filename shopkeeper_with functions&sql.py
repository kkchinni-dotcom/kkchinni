import pymysql
from datetime import datetime

# ---------------- Database Connection ---------------- #
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",          # or your MySQL user
        password="chinni",  # your MySQL password
        database="shopkeeper"    # your database name
        
    )

# ---------------- Helper Functions ---------------- #
def yes_no_input(prompt):
    while True:
        ans = input(prompt).strip().lower()
        if ans in ["yes", "no"]:
            return ans
        print("Please enter only 'yes' or 'no'.")

def validate_veg_name(name):
    return all(ch.isalpha() or ch in [' ', '-'] for ch in name)

# ---------------- Shopkeeper Functions ---------------- #
def add_or_update_vegetable():
    conn = get_connection()
    cursor = conn.cursor()

    while True:
        v = input("Enter vegetable name: ").strip().lower()
        if not validate_veg_name(v):
            print("Invalid name. Only alphabets, spaces, and hyphens allowed.")
            continue

        cursor.execute("SELECT veg_id, quantity, cost_price, sell_price FROM vegetables WHERE name=%s", (v,))
        row = cursor.fetchone()

        if row:
            print(f"{v.title()} already exists with Qty={row[1]}, Cost={row[2]}, Sell={row[3]}")
            update_choice = yes_no_input("Do you want to update this vegetable? (yes/no): ")
            if update_choice == "yes":
                action = input("Update 'quantity', 'price', or 'both': ").lower()
                if action in ["quantity", "both"]:
                    add_qty = float(input("Enter quantity to add: "))
                    cursor.execute("UPDATE Vegetables SET quantity = quantity + %s WHERE veg_id=%s", (add_qty, row[0]))
                if action in ["price", "both"]:
                    cp = float(input("Enter new cost price: "))
                    while True:
                        sp = float(input("Enter new selling price: "))
                        if sp > cp:
                            break
                        print("Selling price must be greater than cost price.")
                    cursor.execute("UPDATE Vegetables SET cost_price=%s, sell_price=%s WHERE veg_id=%s", (cp, sp, row[0]))
                conn.commit()
                print("Vegetable updated successfully.")
        else:
            q = float(input("Enter quantity: "))
            cp = float(input("Enter cost price: "))
            while True:
                sp = float(input("Enter selling price: "))
                if sp > cp:
                    break
                print("Selling price must be greater than cost price.")
            cursor.execute("INSERT INTO Vegetables (name, quantity, cost_price, sell_price) VALUES (%s,%s,%s,%s)", (v, q, cp, sp))
            conn.commit()
            print("Vegetable added successfully.")

        repeat = yes_no_input("Do you want to add/update another vegetable? (yes/no): ")
        if repeat != "yes":
            break

    cursor.close()
    conn.close()

def print_inventory():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, quantity, cost_price, sell_price FROM Vegetables")
    print("\n--- Inventory Report ---")
    for name, qty, cost, sell in cursor.fetchall():
        print(f"{name.title()} | Qty: {qty} | Cost: {cost} | Sell: {sell}")
    cursor.close()
    conn.close()

   

def add_customer():
    conn = get_connection()
    cursor = conn.cursor()

    cname = input("Enter customer name: ").strip().lower()
    cursor.execute("SELECT customer_id FROM Customers WHERE name=%s", (cname,))
    if cursor.fetchone():
        print("Customer already exists.")
        return

    while True:
        cphone = input("Enter phone number (10 digits): ")
        if len(cphone) == 10 and cphone.isdigit():
            cursor.execute("INSERT INTO Customers (name, phone) VALUES (%s,%s)", (cname, cphone))
            conn.commit()
            print("Customer added successfully.")
            break
        else:
            print("Invalid phone number. Try again.")

    cursor.close()
    conn.close()

def view_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id, name, phone FROM customers")
    print("\n--- All customers details ---")
    for CID, name, phone in cursor.fetchall():
        print(f"CID: {CID} | Name: {name} | Phone: {phone}")
    cursor.close()
    conn.close()



def revenue_report():
    conn = get_connection()
    cursor = conn.cursor()

    print("\nRevenue Report Options:")
    print("1. Customer-wise profit")
    print("2. Vegetable-wise profit")
    print("3. Overall profit per day")
    choice = input("Enter choice: ")

    if choice == "1":
        cursor.execute("""
            SELECT c.name, SUM(t.profit) 
            FROM Transactions t 
            JOIN Customers c ON t.customer_id=c.customer_id 
            GROUP BY c.name
        """)
        for name, profit in cursor.fetchall():
            print(f"Customer: {name.title()} | Profit: {profit}")

    elif choice == "2":
        cursor.execute("""
            SELECT v.name, SUM(ti.profit) 
            FROM Transaction_Items ti 
            JOIN Vegetables v ON ti.veg_id=v.veg_id 
            GROUP BY v.name
        """)
        for name, profit in cursor.fetchall():
            print(f"Vegetable: {name.title()} | Profit: {profit}")

    elif choice == "3":
        cursor.execute("SELECT DATE(transaction_date), SUM(profit) FROM Transactions GROUP BY DATE(transaction_date)")
        for day, profit in cursor.fetchall():
            print(f"Date: {day} | Overall Profit: {profit}")
    else:
        print("Invalid choice.")

    cursor.close()
    conn.close()

# ---------------- Customer Functions ---------------- #
def customer_menu():
    conn = get_connection()
    cursor = conn.cursor()
    cart = []

    while True:
        print("\nCustomer Menu")
        print("1. Add item to cart")
        print("2. View cart")
        print("3. Print final bill and exit")
        print("4. Exit without billing")
        choice = input("Enter choice: ")

        if choice == "1":
            print_inventory()
            v = input("Enter vegetable name: ").strip().lower()
            cursor.execute("SELECT veg_id, quantity, cost_price, sell_price FROM Vegetables WHERE name=%s", (v,))
            row = cursor.fetchone()
            if row:
                qty = float(input("Enter quantity: "))
                if qty <= row[1]:
                    cart.append([row[0], v, qty, row[2], row[3]])
                    print("Item added to cart.")
                else:
                    print("Insufficient stock.")
            else:
                print("Vegetable not found.")

        elif choice == "2":
            if not cart:
                print("Cart is empty.")
            else:
                print("\n--- Cart Items ---")
                for _, name, qty, cost, sell in cart:
                    print(f"{name.title()} | Qty: {qty} | Price: {sell} | Total: {qty * sell}")

        elif choice == "3":
            if not cart:
                print("Cart is empty. Cannot generate bill.")
                continue

            cname = input("Enter your name: ").strip().lower()
            cursor.execute("SELECT customer_id FROM Customers WHERE name=%s", (cname,))
            row = cursor.fetchone()
            if not row:
                add_customer()
                cursor.execute("SELECT customer_id FROM Customers WHERE name=%s", (cname,))
                row = cursor.fetchone()
            customer_id = row[0]

            grand_total = 0
            cart_profit = 0
            print("\n--- Final Bill ---")
            for veg_id, name, qty, cost, sell in cart:
                total = qty * sell
                profit = (sell - cost) * qty
                grand_total += total
                cart_profit += profit
                print(f"{name.title()} | Qty: {qty} | Price: {sell} | Total: {total} | Profit: {profit}")
                cursor.execute("UPDATE Vegetables SET quantity = quantity - %s WHERE veg_id=%s", (qty, veg_id))

            cursor.execute("INSERT INTO Transactions (customer_id, total_amount, profit) VALUES (%s,%s,%s)",
                           (customer_id, grand_total, cart_profit))
            conn.commit()
            transaction_id = cursor.lastrowid

            for veg_id, name, qty, cost, sell in cart:
                profit = (sell - cost) * qty
                cursor.execute("""INSERT INTO Transaction_Items 
                                  (transaction_id, veg_id, quantity, cost_price, sell_price, profit) 
                                  VALUES (%s,%s,%s,%s,%s,%s)""",
                               (transaction_id, veg_id, qty, cost, sell, profit))
            conn.commit()

            print("Grand Total:", grand_total)
            print("Profit from this cart:", cart_profit)
            break

        elif choice == "4":
            print("Exit without billing. Cart cleared.")
            break
        else:
            print("Invalid choice.")

    cursor.close()
    conn.close()

# ---------------- Main Program ---------------- #
def main():
    while True:
        print("\nMain Menu")
        print("1. Shopkeeper")
        print("2. Customer")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            # Simple authentication
            if input("Enter username: ") != "chinni" or input("Enter password: ") != "1234":
                print("Access denied.")
                continue

            print("Access granted.")
            while True:
                print("\nShopkeeper Menu")
                print("1. Add/Update vegetable")
                print("2. View inventory")
                print("3. Add customer")
                print("4. View customers")
                print("5. Revenue report")
                print("6. Exit to main menu")
                s_choice = input("Enter choice: ")

                if s_choice == "1":
                    add_or_update_vegetable()
                elif s_choice == "2":
                    print_inventory()
                elif s_choice == "3":
                    add_customer()
                elif s_choice == "4":
                    view_customers()                    
                elif s_choice == "5":
                    revenue_report()
                elif s_choice == "6":
                    break
                else:
                    print("Invalid choice. Try again.")

        elif choice == "2":
            customer_menu()

        elif choice == "3":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Try again.")


# ---------------- Run Program ---------------- #
if __name__ == "__main__":
    main()
