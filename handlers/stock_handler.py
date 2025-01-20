# telegram_bot_inventory/handlers/stock_handler.py
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from keyboards.keyboards import Keyboards
from config.config import Config
from database.database import Database

# Initialize database
db = Database()

async def handle_size_selection(update: Update, context: CallbackContext):
    """
    Handles the size selection step for stock.
    """
    query = update.callback_query
    await query.answer()

    if query.data == 'back':
        # Go back to the action selection step
        await query.edit_message_text(
            text="Choose an action:",
            reply_markup=Keyboards.get_action_keyboard()
        )
        return "ACTION"
    elif query.data == 'home':
        # Go back to the start menu
        await query.edit_message_text(
            text="Welcome! Choose a product:",
            reply_markup=Keyboards.get_products_keyboard()
        )
        return ConversationHandler.END
    else:
        # Save the selected size and proceed to the color selection step
        context.user_data['size'] = query.data.replace('size_', '')
        await query.edit_message_text(
            text="Choose a color:",
            reply_markup=Keyboards.get_colors_keyboard()
        )
        return "COLOR"

async def handle_color_selection(update: Update, context: CallbackContext):
    """
    Handles the color selection step for stock.
    """
    query = update.callback_query
    await query.answer()

    if query.data == 'back':
        # Go back to the size selection step
        await query.edit_message_text(
            text="Choose a size:",
            reply_markup=Keyboards.get_sizes_keyboard()
        )
        return "SIZE"
    elif query.data == 'home':
        # Go back to the start menu
        await query.edit_message_text(
            text="Welcome! Choose a product:",
            reply_markup=Keyboards.get_products_keyboard()
        )
        return ConversationHandler.END
    else:
        # Save the selected color and fetch the stock
        context.user_data['color'] = query.data.replace('color_', '')
        stock = db.get_stock(
            product_id=Config.PRODUCTS.index(context.user_data['product']),
            size=context.user_data['size'],
            color=context.user_data['color']
        )
        await query.edit_message_text(
            text=f"Stock for {context.user_data['product']}, {context.user_data['size']}, {context.user_data['color']}: {stock}",
            reply_markup=Keyboards.get_action_keyboard()
        )
        return ConversationHandler.END