from dotenv import load_dotenv
import os
import mysql.connector
import streamlit as st

load_dotenv()

def create_connection():
    """Creates a new database connection"""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def get_connection():
    """Returns a persistent database connection"""
    if "conn" not in st.session_state or not st.session_state.conn.is_connected():
        st.session_state.conn = create_connection()
    return st.session_state.conn

def close_connection(connection):
    """Closes the database connection"""
    if connection and connection.is_connected():
        connection.close()