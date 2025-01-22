import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Create a table for inventory
cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory (
    product TEXT,
    size TEXT,
    color TEXT,
    quantity INTEGER,
    PRIMARY KEY (product, size, color)
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()