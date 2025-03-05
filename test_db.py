import mysql.connector
import traceback

print("Test script is running!")
print("Attempting to connect to MySQL...")

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Hailxevil0611",
        database="shopping_mart"
    )
    if connection.is_connected():
        print("✅ Connection to MySQL database successful!")
        db_info = connection.get_server_info()
        print(f"Connected to MySQL Server version {db_info}")
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        record = cursor.fetchone()
        print(f"Connected to database: {record}")

except mysql.connector.Error as e:
    print("❌ Error connecting to MySQL:", e)
    print(traceback.format_exc())

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("🔌 MySQL connection closed.")
