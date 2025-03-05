import mysql.connector
import streamlit as st

def create_connection():
    """Creates a new database connection"""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Hailxevil0611",
        database="shopping_mart"
    )

def get_connection():
    """Returns a persistent database connection"""
    if "conn" not in st.session_state or not st.session_state.conn.is_connected():
        st.session_state.conn = create_connection()
    return st.session_state.conn
