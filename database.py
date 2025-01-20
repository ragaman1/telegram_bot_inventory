# database.py
import sqlite3

# Initialize the database
def initialize_database():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Create the products table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            size TEXT NOT NULL,
            color TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Add a product to the database
def add_product(name, size, color, quantity):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Insert the product into the database
    cursor.execute('''
        INSERT INTO products (name, size, color, quantity)
        VALUES (?, ?, ?, ?)
    ''', (name, size, color, quantity))

    conn.commit()
    conn.close()

# Fetch all products from the database
def get_all_products():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Fetch all products
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()

    conn.close()
    return products