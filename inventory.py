# inventory.py
from database import add_product, get_all_products

# Add a new product
def add_new_product(name, size, color, quantity):
    try:
        add_product(name, size, color, quantity)
        return True
    except Exception as e:
        print(f"Error adding product: {e}")
        return False

# Get all products
def get_inventory():
    return get_all_products()