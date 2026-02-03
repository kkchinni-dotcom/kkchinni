# Shopkeeper-Customer Module with Fixes

# Initial Data
veg = ['bringal', 'tamato', 'potatoes', 'carrorts', 'onion']
quantity = [25.0, 35.0, 45.0, 35.0, 55.0]
cost_price = [10, 20, 25, 30, 35]
sell_price = [15, 25, 30, 35, 40]

customers = [['king', '9876543210'], ['krishna', '9876501234'],
             ['raju', '9876549876'], ['rani', '9876509876']]

cart = []
transactions = []

# Helper Functions
def yes_no_input(prompt):
    while True:
        ans = input(prompt).lower()
        if ans in ["yes", "no"]:
            return ans
        else:
            print("Please enter only 'yes' or 'no'.")

def validate_veg_name(name):
    return name.isalpha()

# Main Program
while True:
    print("\nMain Menu")
    print("1. Shopkeeper")
    print("2. Customer")
    print("3. Exit")

    choice = input("Enter choice number: ")

    # SHOPKEEPER SECTION
    if choice == "1":
        U = "Chinni"
        P = "1234"

        while True:
            Username = input("Enter username: ")
            if Username == U:
                break
            else:
                print("Invalid username. Please try again.")

        while True:
            Password = input("Enter password: ")
            if Password == P:
                break
            else:
                print("Incorrect password. Please try again.")

        print("Access Granted")

        while True:
            print("\nShopkeeper Menu")
            print("1. Add vegetable")
            print("2. Modify vegetable")
            print("3. Remove vegetable")
            print("4. View report of items")
            print("5. Add customer")
            print("6. View customers")
            print("7. Revenue report")
            print("8. Exit to main menu")

            s_choice = input("Enter choice: ")

            # Add vegetable
            if s_choice == "1":
                while True:
                    v = input("Enter vegetable name: ")
                    if not validate_veg_name(v):
                        print("Invalid name. Only alphabets allowed.")
                        continue
                    
                    # Check if vegetable already exists
                    if v in veg:
                        idx = veg.index(v)
                        print(f"{v} already exists with Quantity={quantity[idx]}, Cost={cost_price[idx]}, Sell={sell_price[idx]}")
                        update_choice = yes_no_input("Do you want to update this vegetable? (yes/no): ")
                        if update_choice == "yes":
                            # Ask what to update
                            action = input("Update 'quantity', 'price', or 'both': ").lower()
                            if action == "quantity" or action == "both":
                                add_qty = float(input("Enter quantity to add: "))
                                quantity[idx] += add_qty
                                print("Quantity updated successfully.")
                            if action == "price" or action == "both":
                                cp = float(input("Enter new cost price: "))
                                while True:
                                    sp = float(input("Enter new selling price: "))
                                    if sp > cp:
                                        break
                                    else:
                                        print("Selling price should be greater than cost price")
                                cost_price[idx] = cp
                                sell_price[idx] = sp
                                print("Price updated successfully.")
                        else:
                            print("No changes made to existing vegetable.")
                    else:
                        # Add as new vegetable

                        q = float(input("Enter quantity (float): "))
                        cp = float(input("Enter cost price: "))

                        while True:
                            sp = float(input("Enter selling price: "))
                            if sp > cp:
                                break
                            else:
                                print("Selling price should be greater than cost price")

                        veg.append(v)
                        quantity.append(q)
                        cost_price.append(cp)
                        sell_price.append(sp)
                        print("Vegetable added successfully.")

                    repeat = yes_no_input("Do you want to add another vegetable? (yes/no): ")
                    if repeat != "yes":
                        break

            # Modify vegetable
            elif s_choice == "2":
                print(veg)
                while True:
                    vname = input("Enter vegetable name to modify: ")
                    if vname in veg:
                        idx = veg.index(vname)
                        action = input("Do you want to modify 'quantity' or 'price' or 'both'? ").lower()

                        if action == "quantity":
                            qty = float(input("Enter new quantity to add: "))
                            quantity[idx] += qty
                            print("Vegetable quantity updated successfully.")

                        elif action == "price":
                            cp = float(input("Enter new cost price: "))
                            sp = float(input("Enter new selling price: "))
                            if sp > cp:
                                cost_price[idx] = cp
                                sell_price[idx] = sp
                                print("Vegetable price updated successfully.")
                            else:
                                print("Selling price must be greater than cost price.")
                        elif action == "both":
                                qty = float(input("Enter new quantity to add: "))
                                quantity[idx] += qty
                                cp = float(input("Enter new cost price: "))
                                sp = float(input("Enter new selling price: "))
                                if sp > cp:
                                    cost_price[idx] = cp
                                    sell_price[idx] = sp
                                    print("Vegetable quantity and price updated successfully.")
                                else:
                                    print("Selling price must be greater than cost price.")

                        else:
                            print("Invalid option.")
                            

                    else:
                        print("Vegetable not found. Please enter correct name.")

                    repeat = yes_no_input("Do you want to modify another vegetable? (yes/no): ")
                    if repeat != "yes":
                        break

            # Remove vegetable
            elif s_choice == "3":
                print(veg)
                while True:
                    vname = input("Enter vegetable name to remove: ")
                    if vname in veg:
                        idx = veg.index(vname)
                        veg.pop(idx)
                        quantity.pop(idx)
                        cost_price.pop(idx)
                        sell_price.pop(idx)
                        print("Vegetable removed successfully.")
                    else:
                        print("Vegetable not found. Please enter correct name.")

                    repeat = yes_no_input("Do you want to remove another vegetable? (yes/no): ")
                    if repeat != "yes":
                        break

            # View inventory
            elif s_choice == "4":
                print("Report of Items:")
                for name, qty, cp, sp in zip(veg, quantity, cost_price, sell_price):
                    print("Name:", name, "| Quantity:", qty, "| Cost Price:", cp, "| Sell Price:", sp)

            # Add customer
            elif s_choice == "5":
                cname = input("Enter customer name (or type 'exit' to cancel): ")
                if cname.lower() == "exit":
                    print("Cancelled adding customer.")
                    continue

                while True:
                    cphone = input("Enter phone number (10 digits): ")
                    if len(cphone) == 10 and cphone.isdigit() and cphone not in ['1234567890', '9876543210']:
                        customers.append([cname, cphone])
                        print("Customer added.")
                        break
                    else:
                        print("Invalid phone number. Try again.")

            # View customers
            elif s_choice == "6":
                print("Customer List:")
                for c in customers:
                    print("Customer:", c[0], "| Phone:", c[1])

            # Revenue report
            elif s_choice == "7":
                print("Revenue Report Options:")
                print("1. Customer-wise profit")
                print("2. Vegetable-wise profit")
                print("3. Overall profit per day")
                r_choice = input("Enter choice: ")

                if not transactions:
                    print("There are no transactions yet.")
                else:
                    if r_choice == "1":
                        for t in transactions:
                            print("Customer:", t["customer"], "| Profit:", t["profit"])

                    elif r_choice == "2":
                        veg_profit = {}
                        for t in transactions:
                            for name, qty, price in t["items"]:
                                cp = cost_price[veg.index(name)]
                                veg_profit[name] = veg_profit.get(name, 0) + (price - cp) * qty
                        for name, profit in veg_profit.items():
                            print("Vegetable:", name, "| Profit:", profit)

                    elif r_choice == "3":
                        overall = sum(t["profit"] for t in transactions)
                        print("Overall Profit per Day:", overall)

                    else:
                        print("Invalid choice.")

            elif s_choice == "8":
                break
            else:
                print('Wrong option, select right choice')

    # CUSTOMER SECTION
    elif choice == "2":
        while True:
            print("\nCustomer Menu")
            print("1. Add item to cart")
            print("2. Modify item in cart")
            print("3. Delete item from cart")
            print("4. View cart")
            print("5. Print final bill and exit")
            print("6. Exit without billing")

            c_choice = input("Enter choice: ")

            # Add item to cart
            if c_choice == "1":
                while True:
                    for idx, (name, sp, qty) in enumerate(zip(veg, sell_price, quantity)):
                        print(idx, name, "Price:", sp, "| Available:", qty)

                    vname = input("Enter vegetable name to add: ")
                    if vname in veg:
                        idx = veg.index(vname)
                        qty = float(input("Enter quantity: "))
                        if qty <= quantity[idx]:
                            cart.append([veg[idx], qty, sell_price[idx]])
                            quantity[idx] -= qty
                            print("Item added to cart.")
                        else:
                            print("No sufficient quantity available. Only", quantity[idx], "left in stock.")
                    else:
                        print("Vegetable not found. Please enter correct name.")

                    more = yes_no_input("Do you want to add another item? (yes/no): ")
                    if more != "yes":
                        break

            # Modify item in cart
            elif c_choice == "2":
                if not cart:
                    print("Cart is empty. You cannot modify items.")
                else:
                    print(cart)
                    while True:
                        vname = input("Enter vegetable name to modify in cart: ")
                        found = False
                        for idx, item in enumerate(cart):
                            if item[0] == vname:
                                found = True
                                new_qty = float(input("Enter new quantity: "))
                                veg_index = veg.index(vname)
                                available_stock = quantity[veg_index] + cart[idx][1]
                                if new_qty <= available_stock:
                                    quantity[veg_index] += cart[idx][1]
                                    cart[idx][1] = new_qty
                                    quantity[veg_index] -= new_qty
                                    print("Cart updated.")
                                else:
                                    print("No sufficient quantity available. Only", available_stock, "left in stock.")
                                break
                        if not found:
                            print("Vegetable not found in cart. Please enter correct name.")

                        repeat = yes_no_input("Do you want to modify another item? (yes/no): ")
                        if repeat != "yes":
                            break

            # Delete item
            elif c_choice == "3":
                if not cart:
                    print("Cart is empty. You cannot modify items.")
                else:
                    print(cart)
                    while True:
                        vname = input("Enter vegetable name to remove from cart: ")
                        found = False
                        for idx, item in enumerate(cart):
                            if item[0] == vname:
                                found = True
                                veg_index = veg.index(vname)
                                quantity[veg_index] += cart[idx][1]
                                cart.pop(idx)
                                print("Item removed from cart.")
                                break
                        if not found:
                            print("Vegetable not found in cart. Please enter correct name.")

                        repeat = yes_no_input("Do you want to remove another item? (yes/no): ")
                        if repeat != "yes":
                            break

            # View cart
            elif c_choice == "4":
                if not cart:
                    print("Cart is empty.")
                else:
                    print("Cart Items:")
                    for name, qty, price in cart:
                        total = qty * price
                        print("Name:", name, "| Quantity:", qty, "| Price:", price, "| Total:", total)

            # Final bill
            elif c_choice == "5":
                if not cart:
                    print("Cart is empty. Cannot generate bill.")
                    continue

                cname = input("Enter your name: ")
                found = False
                for c in customers:
                    if c[0] == cname:
                        print("Final Bill for:", cname)
                        print("Phone no:", c[1])
                        found = True
                        break

                if not found:
                    while True:
                        cphone = input("Enter phone number (10 digits): ")
                        if len(cphone) == 10 and cphone.isdigit() and cphone not in ['1234567890','9876543210']:
                            customers.append([cname, cphone])
                            print("New customer added:", cname, "| Phone:", cphone)
                            break
                        else:
                            print("Invalid phone number. Try again.")

                grand_total = 0
                cart_profit = 0
                for name, qty, price in cart:
                    total = qty * price
                    grand_total += total
                    cp = cost_price[veg.index(name)]
                    profit = (price - cp) * qty
                    cart_profit += profit
                    print("Name:", name, "| Quantity:", qty, "| Price:", price,
                          "| Total:", total, "| Profit:", profit)

                print("Grand Total:", grand_total)
                print("Profit from this cart:", cart_profit)

                # Record transaction with profit
                transactions.append({"customer": cname, "items": cart.copy(),
                                     "total": grand_total, "profit": cart_profit})
                cart = []
                break

            elif c_choice == "6":
                print("Exit without billing")
                cart = []  # clear cart if exiting
                break

            else:
                print("Wrong option, select right choice")

    # Exit program
    elif choice == "3":
        print("Exiting program...")
        break

    else:
        print("Invalid choice. Try again.")
