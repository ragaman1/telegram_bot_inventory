# telegram_bot_inventory/handlers/product_handler.py
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from keyboards.keyboards import Keyboards
from config.config import Config

# Define conversation states
PRODUCT, ACTION = range(2)

async def handle_product_selection(update: Update, context: CallbackContext):
    """
    Handles the product selection step.
    """
    query = update.callback_query
    await query.answer()

    if query.data == 'home':
        # Go back to the start menu
        await query.edit_message_text(
            text="Welcome! Choose a product:",
            reply_markup=Keyboards.get_products_keyboard()
        )
        return ConversationHandler.END
    else:
        # Save the selected product and proceed to the action step
        product_index = int(query.data.replace('product_', ''))
        context.user_data['product'] = Config.PRODUCTS[product_index]
        await query.edit_message_text(
            text=f"Selected {Config.PRODUCTS[product_index]}. Choose an action:",
            reply_markup=Keyboards.get_action_keyboard()
        )
        return ACTION

async def handle_action_selection(update: Update, context: CallbackContext):
    """
    Handles the action selection step (Inventory or Stock).
    """
    query = update.callback_query
    await query.answer()

    if query.data == 'back':
        # Go back to the product selection step
        await query.edit_message_text(
            text="Choose a product:",
            reply_markup=Keyboards.get_products_keyboard()
        )
        return PRODUCT
    elif query.data == 'home':
        # Go back to the start menu
        await query.edit_message_text(
            text="Welcome! Choose a product:",
            reply_markup=Keyboards.get_products_keyboard()
        )
        return ConversationHandler.END
    else:
        # Save the selected action and proceed to the next step
        context.user_data['action'] = query.data
        if query.data == 'inventory':
            # Proceed to inventory flow
            await query.edit_message_text(
                text="Choose a size:",
                reply_markup=Keyboards.get_sizes_keyboard()
            )
            return "SIZE"  # Next state (to be handled by inventory_handler.py)
        elif query.data == 'stock':
            # Proceed to stock flow
            await query.edit_message_text(
                text="Choose a size:",
                reply_markup=Keyboards.get_sizes_keyboard()
            )
            return "SIZE"  # Next state (to be handled by stock_handler.py)

async def cancel(update: Update, context: CallbackContext):
    """
    Cancels the conversation and returns to the start menu.
    """
    await update.message.reply_text(
        text="Operation cancelled. Use /start to begin again."
    )
    return ConversationHandler.END