# database.py
import sqlite3
from datetime import datetime

# Initialize the database
def initialize_database():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Create the inventory table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            size TEXT NOT NULL,
            color TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        INSERT INTO inventory (name, size, color, quantity, last_updated)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, size, color, quantity, datetime.now()))

    conn.commit()
    conn.close()

# Fetch all inventory from the database
def get_all_inventory():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Fetch all inventory
    cursor.execute('SELECT * FROM inventory')
    inventory = cursor.fetchall()

    conn.close()
    return inventory

# Update a product's quantity and last_updated timestamp
def update_product_quantity(product_id, new_quantity):
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Update the product's quantity and last_updated timestamp
    cursor.execute('''
        UPDATE inventory
        SET quantity = ?, last_updated = ?
        WHERE id = ?
    ''', (new_quantity, datetime.now(), product_id))

    conn.commit()
    conn.close()

# Fetch stock and last_updated timestamp for a specific product, size, and color
def get_stock(product, size, color):
    """Fetch stock and last updated timestamp from database."""
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Query the database for the stock and last_updated timestamp
    cursor.execute('''
    SELECT quantity, last_updated FROM inventory
    WHERE name = ? AND size = ? AND color = ?
    ''', (product, size, color))
    
    result = cursor.fetchone()
    conn.close()
    
    # Return (quantity, last_updated) if found, otherwise (0, None)
    return result if result else (0, None)

# Update or insert a product's stock and last_updated timestamp
def update_inventory(product, size, color, quantity, operation):
    """Update inventory and last_updated timestamp in database."""
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Fetch current stock
    current_stock, _ = get_stock(product, size, color)
    
    if operation == "Add":
        new_stock = current_stock + quantity
    elif operation == "Remove":
        new_stock = max(0, current_stock - quantity)  # Ensure stock doesn't go below 0
    
    # Update or insert the new stock value and last_updated timestamp
    cursor.execute('''
    INSERT OR REPLACE INTO inventory (name, size, color, quantity, last_updated)
    VALUES (?, ?, ?, ?, ?)
    ''', (product, size, color, new_stock, datetime.now()))
    
    conn.commit()
    conn.close()