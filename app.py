import streamlit as st
import mysql.connector
import traceback

try:
    # Debugging output
    st.write("App started successfully!")
    print("App started successfully!")

    # Attempting database connection
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Hailxevil0611",
            database="shopping_mart"
        )
        st.write("Database connected successfully!")
        print("Database connected successfully!")
    except mysql.connector.Error as db_err:
        st.write("Database connection failed! Check terminal for details.")
        print("Database connection error:", db_err)
        connection = None

    # Your existing app code goes here...
    st.title("Shopping Mart Management System")

    if connection:
        st.write("Connected to database!")
    else:
        st.write("Database not connected.")

except Exception as e:
    st.write("An error occurred. Check the terminal.")
    print("Error in app.py:", traceback.format_exc())
