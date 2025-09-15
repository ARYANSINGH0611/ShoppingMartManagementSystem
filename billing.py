from db import create_connection, close_connection

def create_sale(total_amount):
    connection = create_connection()
    sale_id = None
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO Sales (total_price) VALUES (%s)", (total_amount,))
            connection.commit()
            sale_id = cursor.lastrowid
            print(f"Sale recorded successfully with ID: {sale_id}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            close_connection(connection)
    return sale_id

def add_transaction(sale_id, product_id, quantity, subtotal):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO Transactions (sale_id, product_id, quantity, subtotal)
                VALUES (%s, %s, %s, %s)
            """, (sale_id, product_id, quantity, subtotal))
            cursor.execute("UPDATE Products SET stock = stock - %s WHERE id = %s", (quantity, product_id))
            connection.commit()
            print("Transaction recorded successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            close_connection(connection)

def get_sales():
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Sales")
        sales = cursor.fetchall()
        close_connection(connection)
        return sales