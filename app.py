import streamlit as st
import mysql.connector
import traceback
from dotenv import load_dotenv
import os
from decimal import Decimal
from auth import login_user, register_user
from inventory import add_product, update_product, delete_product, get_all_products
from billing import create_sale, add_transaction, get_sales

load_dotenv()

# Debug reload count
if "reload_count" not in st.session_state:
    st.session_state.reload_count = 0
st.session_state.reload_count += 1
print(f"App reloaded {st.session_state.reload_count} times")

# Initialize session state for connection
if "connection" not in st.session_state:
    st.session_state.connection = None
    try:
        st.session_state.connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        st.write("Database connected successfully!")
        print("Database connected successfully!")
    except mysql.connector.Error as db_err:
        st.write("Database connection failed! Check terminal for details.")
        print("Database connection error:", db_err)

# Initialize cart
if "cart" not in st.session_state:
    st.session_state.cart = []

st.title("Shopping Mart Management System")

try:
    if st.session_state.connection:
        # Initialize session state for login
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.role = None

        # Login/Register Section
        if not st.session_state.logged_in:
            st.subheader("Login or Register")
            action = st.radio("Choose action:", ("Login", "Register"))
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if action == "Register":
                role = st.selectbox("Role", ["admin", "billingMember"])
            if action == "Register" and st.button("Register"):
                register_user(username, password, role)
            if action == "Login" and st.button("Login"):
                user = login_user(username, password)
                if user:
                    st.success(f"Welcome, {username}!")
                    st.session_state.logged_in = True
                    st.session_state.username = user['username']
                    st.session_state.role = user['role']
                else:
                    st.error("Invalid credentials!")
        else:
            st.write(f"Logged in as: {st.session_state.username} ({st.session_state.role})")
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.username = None
                st.session_state.role = None
                st.session_state.cart = []  # Clear cart on logout
                st.success("Logged out successfully!")

            # Tabs based on role
            if st.session_state.role == "admin":
                tabs = st.tabs(["Manage Products", "Record Sale", "View Sales"])
            else:  # billingMember
                tabs = st.tabs(["Record Sale", "View Sales"])

            if st.session_state.role == "admin":
                with tabs[0]:
                    st.subheader("Manage Products")
                    st.write("Add New Product")
                    with st.form("add_product_form"):
                        name = st.text_input("Product Name")
                        category = st.text_input("Category")
                        price = st.number_input("Price (₹)", min_value=0.0, step=0.01)
                        stock = st.number_input("Stock", min_value=0, step=1)
                        if st.form_submit_button("Add Product"):
                            if name and price > 0 and stock >= 0:
                                add_product(name, category, price, stock)
                                st.success("Product added!")
                            else:
                                st.error("Please fill all required fields correctly.")

                    st.write("All Products")
                    products = get_all_products()
                    if products:
                        for product in products:
                            st.write(f"ID: {product[0]}, Name: {product[1]}, Category: {product[2]}, Price: ₹{float(product[3]):.2f}, Stock: {product[4]}")
                            if st.button(f"Delete {product[1]}", key=f"delete_{product[0]}"):
                                delete_product(product[0])
                                st.success(f"Deleted {product[1]}")
                    else:
                        st.write("No products found.")

            # Billing Section (accessible to both admin and billingMember)
            with tabs[0 if st.session_state.role == "admin" else 0]:
                st.subheader("Record Sale - Shopping Mart Billing")
                st.write("Enter Customer Details")
                customer_name = st.text_input("Customer Name")
                customer_phone = st.text_input("Customer Phone Number")
                customer_email = st.text_input("Customer Email (optional)")

                st.write("Select Products by Category")
                # Get unique categories
                products = get_all_products()
                categories = sorted(set(product[2] for product in products if product[2]))
                if not categories:
                    st.write("No categories available. Add products with categories in Manage Products.")
                else:
                    selected_category = st.selectbox("Select Category", categories)
                    st.write(f"Products in {selected_category}")
                    category_products = [p for p in products if p[2] == selected_category]
                    
                    if category_products:
                        with st.form("add_to_cart_form"):
                            selected_products = []
                            for product in category_products:
                                quantity = st.number_input(
                                    f"{product[1]} (Price: ₹{float(product[3]):.2f}, Stock: {product[4]})",
                                    min_value=0, step=1, key=f"qty_{product[0]}"
                                )
                                if quantity > 0:
                                    if quantity <= product[4]:
                                        selected_products.append({
                                            'id': product[0],
                                            'name': product[1],
                                            'category': product[2],
                                            'quantity': quantity,
                                            'subtotal': float(product[3]) * quantity
                                        })
                                    else:
                                        st.error(f"Insufficient stock for {product[1]}. Available: {product[4]}")
                            if st.form_submit_button("Add to Cart"):
                                if selected_products:
                                    st.session_state.cart.extend(selected_products)
                                    st.success(f"Added {len(selected_products)} product(s) to cart!")
                                else:
                                    st.error("Please select at least one product with valid quantity.")
                    else:
                        st.write(f"No products found in {selected_category}.")

                # Display Cart
                st.write("Current Cart")
                if st.session_state.cart:
                    total = sum(item['subtotal'] for item in st.session_state.cart)
                    for i, item in enumerate(st.session_state.cart):
                        st.write(f"{item['name']} ({item['category']}) x {item['quantity']} = ₹{item['subtotal']:.2f}")
                        if st.button(f"Remove {item['name']}", key=f"remove_{i}"):
                            st.session_state.cart.pop(i)
                            st.success(f"Removed {item['name']} from cart.")
                            st.rerun()  # Updated from experimental_rerun
                else:
                    st.write("Cart is empty.")
                    total = 0.0

                # GST and Discount
                gst_rate = st.number_input("GST Rate (%)", min_value=0.0, value=0.0, step=0.1)
                discount = st.number_input("Discount (₹)", min_value=0.0, value=0.0, step=0.01)
                total_with_gst = total * (1 + gst_rate / 100) - discount
                st.write(f"Subtotal: ₹{total:.2f}")
                st.write(f"Total with GST ({gst_rate}%): ₹{total_with_gst:.2f}")

                if st.button("Record Sale and Generate Bill"):
                    if st.session_state.cart and customer_name and customer_phone:
                        sale_id = create_sale(total_with_gst)
                        if sale_id:
                            for item in st.session_state.cart:
                                add_transaction(sale_id, item['id'], item['quantity'], item['subtotal'])
                            st.success(f"Sale recorded successfully! Sale ID: {sale_id}")

                            # Generate and Display Bill
                            st.subheader("Generated Bill")
                            from datetime import datetime
                            bill_text = f"""
                            --- Shopping Mart Bill ---
                            Sale ID: {sale_id}
                            Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                            Customer Name: {customer_name}
                            Phone Number: {customer_phone}
                            Email: {customer_email if customer_email else 'N/A'}

                            Items Purchased:
                            """
                            for item in st.session_state.cart:
                                bill_text += f"- {item['name']} ({item['category']}) x {item['quantity']} = ₹{item['subtotal']:.2f}\n"
                            bill_text += f"""
                            Subtotal: ₹{total:.2f}
                            GST ({gst_rate}%): ₹{(total * gst_rate / 100):.2f}
                            Discount: ₹{discount:.2f}
                            Grand Total: ₹{total_with_gst:.2f}

                            Thank you for shopping at Shopping Mart!
                            ---
                            """
                            st.text_area("Bill Details (Copy or Screenshot)", bill_text, height=400)
                            st.session_state.cart = []  # Clear cart after successful sale
                        else:
                            st.error("Failed to record sale.")
                    else:
                        st.error("Please add products to cart, enter customer name and phone number.")

            with tabs[1 if st.session_state.role == "admin" else 1]:
                st.subheader("Sales History")
                sales = get_sales()
                if sales:
                    for sale in sales:
                        st.write(f"Sale ID: {sale[0]}, Total: ₹{float(sale[1]):.2f}, Date: {sale[2]}")
                else:
                    st.write("No sales recorded.")

    else:
        st.write("Database not connected.")

except Exception as e:
    st.write("An error occurred. Check the terminal.")
    print("Error in app.py:", traceback.format_exc())

finally:
    if st.session_state.connection and st.session_state.connection.is_connected():
        st.session_state.connection.close()