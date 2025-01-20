# utils.py
def validate_quantity(quantity):
    try:
        return int(quantity) > 0
    except ValueError:
        return False

def format_inventory(products):
    if not products:
        return "📦 The inventory is empty."

    response = "📦 Inventory:\n\n"
    for product in products:
        response += f"ID: {product[0]}\nName: {product[1]}\nSize: {product[2]}\nColor: {product[3]}\nQuantity: {product[4]}\n\n"
    return response