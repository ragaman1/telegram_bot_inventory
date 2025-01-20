# telegram_bot_inventory/keyboards/keyboards.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config.config import Config

class Keyboards:
    @staticmethod
    def get_products_keyboard():
        """
        Returns a keyboard with product options.
        """
        keyboard = [[InlineKeyboardButton(product, callback_data=f'product_{i}')] 
                   for i, product in enumerate(Config.PRODUCTS)]
        keyboard.append([InlineKeyboardButton("🏠 Home", callback_data='home')])
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_action_keyboard():
        """
        Returns a keyboard with actions (Inventory, Stock, Home).
        """
        keyboard = [
            [InlineKeyboardButton("Inventory", callback_data='inventory')],
            [InlineKeyboardButton("Stock", callback_data='stock')],
            [InlineKeyboardButton("🏠 Home", callback_data='home')]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_sizes_keyboard():
        """
        Returns a keyboard with size options.
        """
        keyboard = [[InlineKeyboardButton(size, callback_data=f'size_{size}')] 
                   for size in Config.SIZES]
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data='back')])
        keyboard.append([InlineKeyboardButton("🏠 Home", callback_data='home')])
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_colors_keyboard():
        """
        Returns a keyboard with color options.
        """
        keyboard = [[InlineKeyboardButton(color, callback_data=f'color_{color}')] 
                   for color in Config.COLORS]
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data='back')])
        keyboard.append([InlineKeyboardButton("🏠 Home", callback_data='home')])
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_quantities_keyboard():
        """
        Returns a keyboard with quantity options.
        """
        keyboard = [[InlineKeyboardButton(str(quantity), callback_data=f'quantity_{quantity}')] 
                   for quantity in Config.QUANTITIES]
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data='back')])
        keyboard.append([InlineKeyboardButton("🏠 Home", callback_data='home')])
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_tags_keyboard():
        """
        Returns a keyboard with tag options.
        """
        keyboard = [[InlineKeyboardButton(tag, callback_data=f'tag_{tag}')] 
                   for tag in Config.TAG]
        keyboard.append([InlineKeyboardButton("🔙 Back", callback_data='back')])
        keyboard.append([InlineKeyboardButton("🏠 Home", callback_data='home')])
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_confirmation_keyboard():
        """
        Returns a keyboard with confirmation options (OK, Cancel, Home).
        """
        keyboard = [
            [InlineKeyboardButton("✅ OK", callback_data='confirm_ok')],
            [InlineKeyboardButton("❌ Cancel", callback_data='confirm_cancel')],
            [InlineKeyboardButton("🔙 Back", callback_data='back')],
            [InlineKeyboardButton("🏠 Home", callback_data='home')]
        ]
        return InlineKeyboardMarkup(keyboard)