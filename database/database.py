#telegram_bot_inventory/database/database.py
import sqlite3
from config.config import Config

class Database:
    def __init__(self):
        self.db_path = Config.DB_PATH

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def add_inventory(self, product_id, size, color, quantity, tag):
        """
        Add a new inventory entry with product_id, size, color, quantity, and tag.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO inventory (product_id, size, color, quantity, tag)
                VALUES (?, ?, ?, ?, ?)
            """, (product_id, size, color, quantity, tag))
            conn.commit()

    def get_stock(self, product_id, size, color):
        """
        Get the total stock quantity for a specific product, size, and color.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT SUM(quantity) FROM inventory 
                WHERE product_id = ? AND size = ? AND color = ?
            """, (product_id, size, color))
            return cursor.fetchone()[0] or 0

    def get_stock_by_tag(self, product_id, size, color, tag):
        """
        Get the stock quantity for a specific product, size, color, and tag.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT SUM(quantity) FROM inventory 
                WHERE product_id = ? AND size = ? AND color = ? AND tag = ?
            """, (product_id, size, color, tag))
            return cursor.fetchone()[0] or 0