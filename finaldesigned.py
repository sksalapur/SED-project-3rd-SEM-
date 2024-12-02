import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import datetime

# File paths
USER_FILE = "users.txt"
ORDER_FILE = "orders.txt"
ADDRESS_FILE = "address.txt"

# Restaurant menus with images
menus = {
    "Virat": {"Chicken Biryani": [200, "chicken_biryani.png"],
              "Veg Fried Rice": [150, "veg_fried_rice.png"],
              "Veg Meals": [120, "veg_meals.png"],
              "Dosa": [50, "dosa.png"]},
    "Panjurli": {"Chicken Biryani": [210, "chicken_biryani.png"],
                 "Veg Fried Rice": [160, "veg_fried_rice.png"],
                 "Veg Meals": [130, "veg_meals.png"],
                 "Dosa": [60, "dosa.png"]},
    "Udupi": {"Chicken Biryani": [220, "chicken_biryani.png"],
              "Veg Fried Rice": [170, "veg_fried_rice.png"],
              "Veg Meals": [140, "veg_meals.png"],
              "Dosa": [70, "dosa.png"]},
    "Durga": {"Chicken Biryani": [230, "chicken_biryani.png"],
              "Veg Fried Rice": [180, "veg_fried_rice.png"],
              "Veg Meals": [150, "veg_meals.png"],
              "Dosa": [80, "dosa.png"]},
}

# File operations
def load_file(file_path):
    try:
        with open(file_path, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def save_file(file_path, data):
    with open(file_path, "w") as file:
        file.writelines(data)

# Main application class
class FoodDeliveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Food Delivery System")
        self.root.geometry("800x600")
        self.root.configure(bg="#f8f9fa")  # Light background color

        self.username = None
        self.cart = []
        self.selected_restaurant = None

        self.show_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_screen()

        # Add an image at the top of the login screen
        try:
            welcome_img = Image.open("welcome.png")
            welcome_img = welcome_img.resize((300, 150))
            welcome_photo = ImageTk.PhotoImage(welcome_img)
            img_label = tk.Label(self.root, image=welcome_photo, bg="#f8f9fa")
            img_label.image = welcome_photo  # Keep a reference to prevent garbage collection
            img_label.pack(pady=10)
        except FileNotFoundError:
            pass

        tk.Label(self.root, text="Login", font=("Arial", 20, "bold"), bg="#f8f9fa").pack(pady=10)

        tk.Label(self.root, text="Username", font=("Arial", 14), bg="#f8f9fa").pack()
        self.username_entry = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.username_entry.pack()

        tk.Label(self.root, text="Password", font=("Arial", 14), bg="#f8f9fa").pack()
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 12), width=30)
        self.password_entry.pack()

        tk.Button(self.root, text="Login", font=("Arial", 12), bg="#007bff", fg="white", command=self.login).pack(pady=5)
        tk.Button(self.root, text="Register", font=("Arial", 12), bg="#28a745", fg="white", command=self.register).pack(pady=5)

        # Bind the Enter key to trigger login
        self.root.bind("<Return>", lambda event: self.login())

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        users = load_file(USER_FILE)
        for user in users:
            if user.strip().split(":")[0] == username and user.strip().split(":")[1] == password:
                self.username = username
                messagebox.showinfo("Login", "Login successful!")
                self.show_main_menu()
                return
        messagebox.showerror("Login", "Invalid username or password!")

    def register(self):
        self.clear_screen()
        tk.Label(self.root, text="Register", font=("Arial", 20, "bold"), bg="#f8f9fa").pack(pady=10)

        self.registration_fields = {}
        for label in ["Username", "Password", "Full Name", "Email", "Phone Number", "Address"]:
            tk.Label(self.root, text=label, font=("Arial", 14), bg="#f8f9fa").pack()
            entry = tk.Entry(self.root, font=("Arial", 12), width=30)
            entry.pack()
            self.registration_fields[label] = entry

        tk.Button(self.root, text="Submit", font=("Arial", 12), bg="#28a745", fg="white", command=self.save_registration).pack(pady=5)

    def save_registration(self):
        data = {label: entry.get() for label, entry in self.registration_fields.items()}

        if not all(data.values()):
            messagebox.showerror("Register", "All fields are required!")
            return

        users = load_file(USER_FILE)
        for user in users:
            if user.split(":")[0] == data["Username"]:
                messagebox.showerror("Register", "Username already exists!")
                return

        users.append(f"{data['Username']}:{data['Password']}\n")
        save_file(USER_FILE, users)

        with open(ADDRESS_FILE, "a") as address_file:
            address_file.write(f"{data['Username']}:{data['Address']}\n")

        messagebox.showinfo("Register", "Registration successful!")
        self.show_login_screen()

    def show_main_menu(self):
        self.clear_screen()

        # Add a banner image to the main menu
        try:
            banner_img = Image.open("banner.png")
            banner_img = banner_img.resize((800, 200))
            banner_photo = ImageTk.PhotoImage(banner_img)
            banner_label = tk.Label(self.root, image=banner_photo, bg="#f8f9fa")
            banner_label.image = banner_photo
            banner_label.pack(pady=10)
        except FileNotFoundError:
            pass

        tk.Label(self.root, text=f"Welcome, {self.username}!", font=("Arial", 20, "bold"), bg="#f8f9fa").pack(pady=10)

        tk.Button(self.root, text="Place an Order", font=("Arial", 14), bg="#007bff", fg="white", command=self.place_order).pack(pady=5)
        tk.Button(self.root, text="View Order History", font=("Arial", 14), bg="#17a2b8", fg="white", command=self.view_order_history).pack(pady=5)
        tk.Button(self.root, text="Logout", font=("Arial", 14), bg="#dc3545", fg="white", command=self.logout).pack(pady=5)

    # Implement other methods (place_order, view_order_history, etc.) similarly as earlier...
    def place_order(self):
        self.clear_screen()
        tk.Label(self.root, text="Select a Restaurant", font=("Arial", 16)).pack(pady=10)

        self.restaurant_var = tk.StringVar(value="Virat")
        for restaurant in menus.keys():
            tk.Radiobutton(self.root, text=restaurant, variable=self.restaurant_var, value=restaurant, command=self.display_menu).pack(anchor="w")

        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack()
        self.display_menu()

        tk.Button(self.root, text="View Cart", command=self.view_cart).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=5)

    def display_menu(self):
        for widget in self.menu_frame.winfo_children():
            widget.destroy()

        restaurant = self.restaurant_var.get()

        if self.cart and self.selected_restaurant != restaurant:
            messagebox.showerror("Error", "You can only switch restaurants if the cart is empty!")
            self.restaurant_var.set(self.selected_restaurant)
            return

        self.selected_restaurant = restaurant

        tk.Label(self.menu_frame, text=f"Menu for {restaurant}", font=("Arial", 14)).pack()
        menu = menus[restaurant]
        for dish, (price, image_path) in menu.items():
            frame = tk.Frame(self.menu_frame)
            frame.pack(anchor="w", pady=5)

            img = Image.open(image_path)
            img = img.resize((100, 100))
            img = ImageTk.PhotoImage(img)

            img_label = tk.Label(frame, image=img)
            img_label.image = img
            img_label.pack(side="left")

            tk.Label(frame, text=f"{dish} - ₹{price}").pack(side="left")

            quantity = tk.IntVar(value=1)
            tk.Spinbox(frame, from_=1, to=10, textvariable=quantity).pack(side="left")

            tk.Button(frame, text="Add to Cart", command=lambda d=dish, p=price, q=quantity: self.add_to_cart(d, p, q)).pack(side="left")

    def add_to_cart(self, dish, price, quantity):
        for item in self.cart:
            if item[0] == dish and item[3] == self.selected_restaurant:
                item[2] += quantity.get()
                messagebox.showinfo("Cart", f"Updated {dish} quantity to {item[2]}!")
                return

        self.cart.append([dish, price, quantity.get(), self.selected_restaurant])
        messagebox.showinfo("Cart", f"Added {dish} (x{quantity.get()}) to the cart!")

    def remove_from_cart(self, dish):
        for item in self.cart:
            if item[0] == dish:
                if item[2] > 1:
                    item[2] -= 1
                    messagebox.showinfo("Cart", f"Reduced {dish} quantity to {item[2]}!")
                else:
                    self.cart.remove(item)
                    messagebox.showinfo("Cart", f"Removed {dish} from the cart!")
                break  # Exit the loop once the dish is processed

        # Refresh the cart display
        self.view_cart()


    def view_cart(self):
        self.clear_screen()
        tk.Label(self.root, text="Your Cart", font=("Arial", 16)).pack(pady=10)

        if not self.cart:
            tk.Label(self.root, text="Your cart is empty.").pack(pady=10)
        else:
            tk.Label(self.root, text=f"Restaurant: {self.selected_restaurant}", font=("Arial", 12)).pack(pady=5)

            total_price = 0
            for dish, price, quantity, restaurant in self.cart:
                total_price += price * quantity

                frame = tk.Frame(self.root)
                frame.pack(anchor="w", pady=5)

                tk.Label(frame, text=f"{dish} (x{quantity}) - ₹{price * quantity}").pack(side="left")
                tk.Button(frame, text=f"Remove {dish}", command=lambda d=dish: self.remove_from_cart(d)).pack(side="left")

            tk.Label(self.root, text=f"Total: ₹{total_price}", font=("Arial", 12)).pack(pady=10)

        tk.Button(self.root, text="Confirm Order", command=self.confirm_order).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.place_order).pack(pady=5)


    def confirm_order(self):
        if not self.cart:
            messagebox.showerror("Order", "Your cart is empty!")
            return

        # Create a new window for address and payment
        confirm_window = tk.Toplevel(self.root)
        confirm_window.title("Confirm Order")

        tk.Label(confirm_window, text="Confirm Address", font=("Arial", 14)).pack(pady=5)

        # Retrieve all addresses for the user
        # Retrieve all addresses for the user
        user_addresses = []
        addresses = load_file(ADDRESS_FILE)
        for address in addresses:
            try:
                user, addr = address.strip().split(":")
                if user == self.username:
                    user_addresses.append(addr)
            except ValueError:
                print(f"Skipping malformed address line: {address.strip()}")


        # Variable to track selected or new address
        selected_address = tk.StringVar(value=user_addresses[0] if user_addresses else "")

        # Display previously saved addresses
        if user_addresses:
            tk.Label(confirm_window, text="Select a previous address:", font=("Arial", 12)).pack(pady=5)
            for addr in user_addresses:
                tk.Radiobutton(confirm_window, text=addr, variable=selected_address, value=addr).pack(anchor="w")

        # Option to enter a new address
        tk.Label(confirm_window, text="Or enter a new address:", font=("Arial", 12)).pack(pady=5)
        new_address_var = tk.StringVar(value="")
        tk.Entry(confirm_window, textvariable=new_address_var, width=50).pack(pady=5)

        # Payment options
        tk.Label(confirm_window, text="Select Payment Method", font=("Arial", 14)).pack(pady=5)
        payment_var = tk.StringVar(value="Cash on Delivery")
        payment_methods = ["Cash on Delivery", "Credit/Debit Card", "UPI"]
        for method in payment_methods:
            tk.Radiobutton(confirm_window, text=method, variable=payment_var, value=method).pack(anchor="w")

        # Confirm button
        tk.Button(confirm_window, text="Place Order",
                command=lambda: self.finalize_order(selected_address.get(), new_address_var.get(), payment_var.get(), confirm_window)).pack(pady=10)

    def finalize_order(self, selected_address, new_address, payment_method, window):
    # Determine the final address
        final_address = new_address.strip() if new_address.strip() else selected_address
        if not final_address:
            messagebox.showerror("Order", "Address cannot be empty!")
            return

        # Load addresses and add new ones if necessary
        addresses = load_file(ADDRESS_FILE)
        formatted_new_address = f"{self.username}:{final_address}\n"

        if formatted_new_address not in addresses:
            addresses.append(formatted_new_address)
            save_file(ADDRESS_FILE, addresses)

        # Save the order details
        orders = load_file(ORDER_FILE)
        total_price = sum(item[1] * item[2] for item in self.cart)
        order = f"{self.username}|{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}|{self.selected_restaurant}|{','.join(f'{d}x{q}' for d, p, q, r in self.cart)}|{total_price}|{payment_method}|{final_address}\n"
        orders.append(order)
        save_file(ORDER_FILE, orders)

        # Reset the cart and close the confirmation window
        self.cart = []
        self.selected_restaurant = None
        window.destroy()

        messagebox.showinfo("Order", "Order placed successfully!")
        self.show_main_menu()




    def view_order_history(self):
        self.clear_screen()
        tk.Label(self.root, text="Order History", font=("Arial", 16)).pack(pady=10)

        orders = load_file(ORDER_FILE)
        has_orders = False

        for order in orders:
            try:
                # Parse the order line using the new delimiter
                user, date, restaurant, items, total, payment, address = order.strip().split("|")
                
                if user == self.username:
                    # Display the order
                    tk.Label(
                        self.root,
                        text=f"Date: {date}, Restaurant: {restaurant}, Items: {items}, Total: ₹{total}, Payment: {payment}, Address: {address}"
                    ).pack(anchor="w")
                    has_orders = True
            except ValueError:
                # Log malformed lines
                print(f"Skipping malformed order line: {order.strip()}")

        if not has_orders:
            tk.Label(self.root, text="You have no past orders.").pack(pady=10)

        tk.Button(self.root, text="Back", command=self.show_main_menu).pack(pady=5)


    def logout(self):
        self.username = None
        self.cart = []
        self.selected_restaurant = None
        messagebox.showinfo("Logout", "Logged out successfully!")
        self.show_login_screen()
if __name__ == "__main__":

    root = tk.Tk()

    app = FoodDeliveryApp(root)

    root.mainloop()

		

