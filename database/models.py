#telegram_bot_inventory/database/models.py
import sqlite3
from config.config import Config

def init_db():
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()
    
    # Create tables
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            size TEXT,
            color TEXT,
            quantity INTEGER,
            tag TEXT,            
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
    ''')
    
    conn.commit()
    conn.close()