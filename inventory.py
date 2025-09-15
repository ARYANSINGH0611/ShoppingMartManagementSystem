from db import create_connection, close_connection

def add_product(name, category, price, stock):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO Products (name, category, price, stock) 
                VALUES (%s, %s, %s, %s)
            """, (name, category, price, stock))
            connection.commit()
            print("Product added successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            close_connection(connection)

def update_product(product_id, name=None, category=None, price=None, stock=None):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            updates = []
            values = []
            if name:
                updates.append("name = %s")
                values.append(name)
            if category:
                updates.append("category = %s")
                values.append(category)
            if price:
                updates.append("price = %s")
                values.append(price)
            if stock:
                updates.append("stock = %s")
                values.append(stock)
            
            values.append(product_id)
            
            query = f"UPDATE Products SET {', '.join(updates)} WHERE product_id = %s"
            cursor.execute(query, values)
            connection.commit()
            print("Product updated successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            close_connection(connection)

def delete_product(product_id):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM Products WHERE product_id = %s", (product_id,))
            connection.commit()
            print("Product deleted successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            close_connection(connection)

def get_all_products():
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
        close_connection(connection)
        return products

if __name__ == "__main__":
    # Example usage
    add_product("Apple", "Fruits", 1.50, 100)
    update_product(1, stock=120)
    print(get_all_products())
    delete_product(1)