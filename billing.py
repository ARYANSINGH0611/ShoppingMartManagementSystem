from db import create_connection, close_connection

def create_sale(total_amount):
    """Creates a sale record and returns the sale ID."""
    connection = create_connection()
    sale_id = None
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO Sales (total_amount) VALUES (%s)", (total_amount,))
            connection.commit()
            sale_id = cursor.lastrowid
            print(f"Sale recorded successfully with ID: {sale_id}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            close_connection(connection)
    return sale_id

def add_transaction(sale_id, product_id, quantity, subtotal):
    """Adds a transaction (product purchase) to a sale."""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO Transactions (sale_id, product_id, quantity, subtotal)
                VALUES (%s, %s, %s, %s)
            """, (sale_id, product_id, quantity, subtotal))
            
            cursor.execute("UPDATE Products SET stock = stock - %s WHERE product_id = %s", (quantity, product_id))
            connection.commit()
            print("Transaction recorded successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            close_connection(connection)

def get_sales():
    """Retrieves all sales records."""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Sales")
        sales = cursor.fetchall()
        close_connection(connection)
        return sales

if __name__ == "__main__":
    # Example usage
    sale_id = create_sale(50.00)
    if sale_id:
        add_transaction(sale_id, 1, 2, 20.00)
    print(get_sales())
