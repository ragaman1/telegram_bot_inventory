import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Bot Configuration
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    
    # Database Configuration
    DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'inventory.db')
    
    # Product Configuration
    PRODUCTS = ['Product 1', 'Product 2']
    SIZES = ['Size 1', 'Size 2', 'Size 3', 'Size 4']
    COLORS = ['Color 1', 'Color 2', 'Color 3', 'Color 4', 'Color 5']
    QUANTITIES = [1, 2, 3, 4, 5]
    TAG = ['place1', 'place2']