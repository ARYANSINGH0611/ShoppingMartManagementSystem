import streamlit as st
import bcrypt
from db import get_connection

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def register_user(username, password, role='billingMember'):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", 
                      (username, hashed_password, role))
        conn.commit()
        st.success("User registered successfully!")
    except Exception as e:
        st.error(f"Registration failed: {e}")
    finally:
        cursor.close()
        conn.close()

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result and bcrypt.checkpw(password.encode(), result[0].encode()):
        return {'username': username, 'role': result[1]}
    return None