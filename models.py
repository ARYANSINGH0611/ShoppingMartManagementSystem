from db import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        stock INT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INT AUTO_INCREMENT PRIMARY KEY,
        product_id INT,
        quantity INT NOT NULL,
        total_price DECIMAL(10,2) NOT NULL,
        sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
    """)

    conn.commit()

if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")
