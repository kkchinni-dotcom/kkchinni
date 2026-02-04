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
        # Reject empty string or names with spaces
        if not v or " " in v or not validate_veg_name(v):
            print("Invalid name. Only alphabets and hyphens allowed, no spaces.")
            continue

        cursor.execute("SELECT veg_id, quantity, cost_price, sell_price FROM Vegetables WHERE name=%s", (v,))
        row = cursor.fetchone()

        if row:
            print(f"{v.title()} already exists with Qty={row[1]}, Cost={row[2]}, Sell={row[3]}")
            update_choice = yes_no_input("Do you want to update this vegetable? (yes/no): ")
            if update_choice == "yes":
                action = input("Update 'quantity', 'price', or 'both': ").lower()
                if action in ["quantity", "both"]:
                    while True:
                        qty_input = input("Enter quantity to add: ").strip()
                        if qty_input.replace('.', '', 1).isdigit():
                            add_qty = float(qty_input)
                            break
                        else:
                            print("Enter valid quantity (numeric only).")
                    cursor.execute("UPDATE Vegetables SET quantity = quantity + %s WHERE veg_id=%s", (add_qty, row[0]))
                if action in ["price", "both"]:
                    while True:
                        cp_input = input("Enter new cost price: ").strip()
                        if cp_input.replace('.', '', 1).isdigit():
                            cp = float(cp_input)
                            break
                        else:
                            print("Enter valid cost price (numeric only).")
                    while True:
                        sp_input = input("Enter new selling price: ").strip()
                        if sp_input.replace('.', '', 1).isdigit():
                            sp = float(sp_input)
                            if sp > cp:
                                break
                            else:
                                print("Selling price must be greater than cost price.")
                        else:
                            print("Enter valid selling price (numeric only).")
                    cursor.execute("UPDATE Vegetables SET cost_price=%s, sell_price=%s WHERE veg_id=%s", (cp, sp, row[0]))
                conn.commit()
                print("Vegetable updated successfully.")
        else:
            while True:
                qty_input = input("Enter quantity: ").strip()
                if qty_input.replace('.', '', 1).isdigit():
                    q = float(qty_input)
                    break
                else:
                    print("Enter valid quantity (numeric only).")
            while True:
                cp_input = input("Enter cost price: ").strip()
                if cp_input.replace('.', '', 1).isdigit():
                    cp = float(cp_input)
                    break
                else:
                    print("Enter valid cost price (numeric only).")
            while True:
                sp_input = input("Enter selling price: ").strip()
                if sp_input.replace('.', '', 1).isdigit():
                    sp = float(sp_input)
                    if sp > cp:
                        break
                    else:
                        print("Selling price must be greater than cost price.")
                else:
                    print("Enter valid selling price (numeric only).")
            cursor.execute("INSERT INTO Vegetables (name, quantity, cost_price, sell_price) VALUES (%s,%s,%s,%s)", (v, q, cp, sp))
            conn.commit()
            print("Vegetable added successfully.")

        repeat = yes_no_input("Do you want to add/update another vegetable? (yes/no): ")
        if repeat != "yes":
            break

    cursor.close()
    conn.close()


def remove_vegetable():
    conn = get_connection()
    cursor = conn.cursor()

    while True:
        # Show current inventory before removal
        cursor.execute("SELECT veg_id, name, quantity, cost_price, sell_price FROM Vegetables")
        rows = cursor.fetchall()
        print("\n--- Current Inventory ---")
        for veg_id, name, qty, cost, sell in rows:
            print(f"ID: {veg_id} | Name: {name.title()} | Qty: {qty} | Cost: {cost} | Sell: {sell}")

        v = input("Enter vegetable name to remove: ").strip().lower()

        # Reject empty or space-only names
        if not v or " " in v or not validate_veg_name(v):
            print("Invalid name. Please enter a valid vegetable name (alphabets and hyphens only, no spaces).")
            continue

        cursor.execute("SELECT veg_id FROM Vegetables WHERE name=%s", (v,))
        row = cursor.fetchone()

        if row:
            cursor.execute("DELETE FROM Vegetables WHERE veg_id=%s", (row[0],))
            conn.commit()
            print(f"{v.title()} removed successfully.")
        else:
            print("Vegetable not found in inventory.")

        repeat = yes_no_input("Do you want to remove another vegetable? (yes/no): ")
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

def remove_customer():
    conn = get_connection()
    cursor = conn.cursor()

    while True:
        # Show current customers before removal
        cursor.execute("SELECT customer_id, name, phone FROM Customers")
        rows = cursor.fetchall()
        print("\n--- Current Customers ---")
        for cid, name, phone in rows:
            print(f"ID: {cid} | Name: {name.title()} | Phone: {phone}")

        cname = input("Enter customer name to remove: ").strip().lower()

        # Reject empty or space-only names
        if not cname or " " in cname or not validate_veg_name(cname):
            print("Invalid name. Please enter a valid customer name (alphabets and hyphens only, no spaces).")
            continue

        cursor.execute("SELECT customer_id FROM Customers WHERE name=%s", (cname,))
        row = cursor.fetchone()

        if row:
            customer_id = row[0]

            # Safety check: does this customer have transactions?
            cursor.execute("SELECT COUNT(*) FROM Transactions WHERE customer_id=%s", (customer_id,))
            txn_count = cursor.fetchone()[0]

            if txn_count > 0:
                print(f"Cannot remove '{cname.title()}'. This customer has {txn_count} transaction(s) recorded.")
            else:
                cursor.execute("DELETE FROM Customers WHERE customer_id=%s", (customer_id,))
                conn.commit()
                print(f"Customer '{cname.title()}' removed successfully.")
        else:
            print("Customer not found in records.")

        repeat = yes_no_input("Do you want to remove another customer? (yes/no): ")
        if repeat != "yes":
            break

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


def shopkeeper_menu():
    conn = get_connection()
    cursor = conn.cursor()
    cart = []
    while True:
        print("\nShopkeeper Menu")
        print("1. Add/Update vegetable")
        print("2. Remove vegetable")
        print("3. View inventory")
        print("4. Add customer")
        print("5. View customers")
        print("6. remove customer")
        print("7. Revenue report")
        print("8. Exit to main menu")
        s_choice = input("Enter choice: ")

        if s_choice == "1":
            add_or_update_vegetable()
        elif s_choice == "2":
            remove_vegetable()
        elif s_choice == "3":
            print_inventory()
        elif s_choice == "4":
            add_customer()
        elif s_choice == "5":
            view_customers()
        elif s_choice == "6":
            remove_customer()
        elif s_choice == "7":
            revenue_report()
        elif s_choice == "8":
            break
        else:
            print("Invalid choice. Try again.")
    
    cursor.close()
    conn.close()

    

# ---------------- Customer Functions ---------------- #

# ---------------- Customer Functions ---------------- #

from decimal import Decimal

def add_item_to_cart(cursor, cart):
    print_inventory()
    v = input("Enter vegetable name: ").strip().lower()
    cursor.execute("SELECT veg_id, quantity, cost_price, sell_price FROM Vegetables WHERE name=%s", (v,))
    row = cursor.fetchone()

    if not row:
        print("Vegetable not found.")
        return

    available_qty = Decimal(str(row[1]))

    while True:
        qty_input = input("Enter quantity: ").strip()
        if qty_input.isdigit() or qty_input.replace('.', '', 1).isdigit():
            qty = Decimal(qty_input)

            # Check against available stock
            if qty <= available_qty:
                cart.append([row[0], v, qty, Decimal(str(row[2])), Decimal(str(row[3]))])
                print(f"{v.title()} added to cart with Qty={qty}.")
                return
            else:
                print(f"Insufficient stock. Only {available_qty} available.")
        else:
            print("Invalid quantity. Enter numeric only.")


def view_cart(cart):
    if not cart:
        print("Cart is empty.")
        return
    print("\n--- Cart Items ---")
    for _, name, qty, cost, sell in cart:
        total = qty * sell
        print(f"{name.title()} | Qty: {qty} | Price: {sell} | Total: {total}")


def modify_cart_item(cursor, cart):
    if not cart:
        print("Cart is empty.")
        return

    view_cart(cart)
    item_name = input("Enter item name to modify: ").strip().lower()

    for item in cart:
        if item[1] == item_name:
            # Fetch current stock from DB
            cursor.execute("SELECT quantity FROM Vegetables WHERE name=%s", (item_name,))
            row = cursor.fetchone()

            if not row:
                print("Item not available in inventory.")
                return

            available_qty = Decimal(str(row[0]))

            while True:
                qty_input = input("Enter new quantity: ").strip()
                if qty_input.isdigit() or qty_input.replace('.', '', 1).isdigit():
                    new_qty = Decimal(qty_input)

                    # Check against available stock
                    if new_qty <= available_qty:
                        item[2] = new_qty
                        print(f"{item_name.title()} quantity updated to {new_qty}.")
                        return
                    else:
                        print(f"Insufficient stock. Only {available_qty} available.")
                else:
                    print("Invalid quantity. Enter numeric only.")
            return

    print("Item not available in cart.")

def remove_cart_item(cart):
    if not cart:
        print("Cart is empty.")
        return
    view_cart(cart)
    item_name = input("Enter item name to remove: ").strip().lower()
    for item in cart:
        if item[1] == item_name:
            cart.remove(item)
            print(f"{item_name.title()} removed from cart.")
            return
    print("Item not available in cart.")


def generate_bill(cursor, conn, cart):
    if not cart:
        print("Cart is empty. Cannot generate bill.")
        return

    cname = input("Enter your name: ").strip().lower()
    cursor.execute("SELECT customer_id FROM Customers WHERE name=%s", (cname,))
    row = cursor.fetchone()

    if not row:
        # Add customer directly without asking name again
        while True:
            cphone = input("Enter phone number (10 digits): ")
            if len(cphone) == 10 and cphone.isdigit():
                try:
                    cursor.execute("INSERT INTO Customers (name, phone) VALUES (%s,%s)", (cname, cphone))
                    conn.commit()
                    print("Customer added successfully.")
                    break
                except pymysql.err.IntegrityError:
                    print("Customer exists with same phone number. Please enter valid phone number.")
            else:
                print("Invalid phone number. Try again.")
        cursor.execute("SELECT customer_id FROM Customers WHERE name=%s", (cname,))
        row = cursor.fetchone()

    customer_id = row[0]
    grand_total = Decimal("0.00")
    cart_profit = Decimal("0.00")

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
    #print("Profit from this cart:", cart_profit)


def customer_menu():
    conn = get_connection()
    cursor = conn.cursor()
    cart = []

    while True:
        print("\nCustomer Menu")
        print("1. Add item to cart")
        print("2. View cart")
        print("3. Modify cart item")
        print("4. Remove cart item")
        print("5. Print final bill and exit")
        print("6. Exit without billing")

        choice = input("Enter choice: ")

        if choice == "1":
            add_item_to_cart(cursor, cart)
        elif choice == "2":
            view_cart(cart)
        elif choice == "3":
            modify_cart_item(cursor, cart)
        elif choice == "4":
            remove_cart_item(cart)
        elif choice == "5":
            generate_bill(cursor, conn, cart)
            break   # Exit after billing
        elif choice == "6":
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
            shopkeeper_menu()
            
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
