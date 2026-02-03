
# Shopkeeper-Customer Module (Refactored)

# Inventory stored as dictionary
inventory = {
    "brinjal": {"quantity": 25.0, "cost": 10, "sell": 15},
    "tomato": {"quantity": 35.0, "cost": 20, "sell": 25},
    "potato": {"quantity": 45.0, "cost": 25, "sell": 30},
    "carrot": {"quantity": 35.0, "cost": 30, "sell": 35},
    "onion": {"quantity": 55.0, "cost": 35, "sell": 40},
}

customers = {
    "king": "9876543210",
    "krishna": "9876501234",
    "raju": "9876549876",
    "rani": "9876509876",
}

transactions = []


# ---------------- Helper Functions ---------------- #

def yes_no_input(prompt):
    while True:
        ans = input(prompt).strip().lower()
        if ans in ["yes", "no"]:
            return ans
        print("Please enter only 'yes' or 'no'.")


def validate_veg_name(name):
    # Allow alphabets, spaces, and hyphens
    return all(ch.isalpha() or ch in [' ', '-'] for ch in name)


def print_inventory():
    print("\n--- Inventory Report ---")
    for name, data in inventory.items():
        print(f"{name.title()} | Qty: {data['quantity']} | Cost: {data['cost']} | Sell: {data['sell']}")


def print_customers():
    print("\n--- Customer List ---")
    for name, phone in customers.items():
        print(f"{name.title()} | Phone: {phone}")


# ---------------- Shopkeeper Functions ---------------- #

def add_or_update_vegetable():
    while True:
        v = input("Enter vegetable name: ").strip().lower()
        if not validate_veg_name(v):
            print("Invalid name. Only alphabets, spaces, and hyphens allowed.")
            continue

        if v in inventory:
            print(f"{v.title()} already exists with Qty={inventory[v]['quantity']}, "
                  f"Cost={inventory[v]['cost']}, Sell={inventory[v]['sell']}")
            update_choice = yes_no_input("Do you want to update this vegetable? (yes/no): ")
            if update_choice == "yes":
                action = input("Update 'quantity', 'price', or 'both': ").lower()
                if action in ["quantity", "both"]:
                    add_qty = float(input("Enter quantity to add: "))
                    inventory[v]['quantity'] += add_qty
                if action in ["price", "both"]:
                    cp = float(input("Enter new cost price: "))
                    while True:
                        sp = float(input("Enter new selling price: "))
                        if sp > cp:
                            break
                        print("Selling price must be greater than cost price.")
                    inventory[v]['cost'] = cp
                    inventory[v]['sell'] = sp
                print("Vegetable updated successfully.")
        else:
            q = float(input("Enter quantity: "))
            cp = float(input("Enter cost price: "))
            while True:
                sp = float(input("Enter selling price: "))
                if sp > cp:
                    break
                print("Selling price must be greater than cost price.")
            inventory[v] = {"quantity": q, "cost": cp, "sell": sp}
            print("Vegetable added successfully.")

        repeat = yes_no_input("Do you want to add/update another vegetable? (yes/no): ")
        if repeat != "yes":
            break


def remove_vegetable():
    print_inventory()
    while True:
        v = input("Enter vegetable name to remove: ").strip().lower()
        if v in inventory:
            del inventory[v]
            print("Vegetable removed successfully.")
        else:
            print("Vegetable not found.")
        repeat = yes_no_input("Do you want to remove another vegetable? (yes/no): ")
        if repeat != "yes":
            break


def add_customer():
    cname = input("Enter customer name: ").strip().lower()
    if cname in customers:
        print("Customer already exists.")
        return
    while True:
        cphone = input("Enter phone number (10 digits): ")
        if len(cphone) == 10 and cphone.isdigit() and cphone not in customers.values():
            customers[cname] = cphone
            print("Customer added successfully.")
            break
        else:
            print("Invalid phone number. Try again.")


def revenue_report():
    if not transactions:
        print("No transactions yet.")
        return

    print("\nRevenue Report Options:")
    print("1. Customer-wise profit")
    print("2. Vegetable-wise profit")
    print("3. Overall profit per day")
    choice = input("Enter choice: ")

    if choice == "1":
        for t in transactions:
            print(f"Customer: {t['customer']} | Profit: {t['profit']}")
    elif choice == "2":
        veg_profit = {}
        for t in transactions:
            for item in t["items"]:
                name, qty, cost, sell = item
                veg_profit[name] = veg_profit.get(name, 0) + (sell - cost) * qty
        for name, profit in veg_profit.items():
            print(f"Vegetable: {name.title()} | Profit: {profit}")
    elif choice == "3":
        overall = sum(t["profit"] for t in transactions)
        print("Overall Profit per Day:", overall)
    else:
        print("Invalid choice.")


# ---------------- Customer Functions ---------------- #

def customer_menu():
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
            if v in inventory:
                qty = float(input("Enter quantity: "))
                if qty <= inventory[v]['quantity']:
                    cart.append([v, qty, inventory[v]['cost'], inventory[v]['sell']])
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
                for name, qty, cost, sell in cart:
                    print(f"{name.title()} | Qty: {qty} | Price: {sell} | Total: {qty * sell}")

        elif choice == "3":
            if not cart:
                print("Cart is empty. Cannot generate bill.")
                continue
            cname = input("Enter your name: ").strip().lower()
            if cname not in customers:
                add_customer()
            grand_total = 0
            cart_profit = 0
            print("\n--- Final Bill ---")
            for name, qty, cost, sell in cart:
                total = qty * sell
                grand_total += total
                profit = (sell - cost) * qty
                cart_profit += profit
                print(f"{name.title()} | Qty: {qty} | Price: {sell} | Total: {total} | Profit: {profit}")
                inventory[name]['quantity'] -= qty  # Deduct stock only now
            print("Grand Total:", grand_total)
            print("Profit from this cart:", cart_profit)
            transactions.append({"customer": cname, "items": cart.copy(),
                                 "total": grand_total, "profit": cart_profit})
            break

        elif choice == "4":
            print("Exit without billing. Cart cleared.")
            break
        else:
            print("Invalid choice.")


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
                print("2. Remove vegetable")
                print("3. View inventory")
                print("4. Add customer")
                print("5. View customers")
                print("6. Revenue report")
                print("7. Exit to main menu")
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
                    print_customers
                elif s_choice == "6":
                    revenue_report()
                elif s_choice == "7":
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
#if __name__ == "__main__":
main()




