# telegram_bot_inventory/handlers/inventory_handler.py
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from keyboards.keyboards import Keyboards
from config.config import Config
from database.database import Database

# Initialize database
db = Database()

async def handle_size_selection(update: Update, context: CallbackContext):
    """
    Handles the size selection step for inventory.
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
    Handles the color selection step for inventory.
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
        # Save the selected color and proceed to the quantity selection step
        context.user_data['color'] = query.data.replace('color_', '')
        await query.edit_message_text(
            text="Choose a quantity:",
            reply_markup=Keyboards.get_quantities_keyboard()
        )
        return "QUANTITY"

async def handle_quantity_selection(update: Update, context: CallbackContext):
    """
    Handles the quantity selection step for inventory.
    """
    query = update.callback_query
    await query.answer()

    if query.data == 'back':
        # Go back to the color selection step
        await query.edit_message_text(
            text="Choose a color:",
            reply_markup=Keyboards.get_colors_keyboard()
        )
        return "COLOR"
    elif query.data == 'home':
        # Go back to the start menu
        await query.edit_message_text(
            text="Welcome! Choose a product:",
            reply_markup=Keyboards.get_products_keyboard()
        )
        return ConversationHandler.END
    else:
        # Save the selected quantity and proceed to the tag selection step
        context.user_data['quantity'] = int(query.data.replace('quantity_', ''))
        await query.edit_message_text(
            text="Choose a tag:",
            reply_markup=Keyboards.get_tags_keyboard()
        )
        return "TAG"

async def handle_tag_selection(update: Update, context: CallbackContext):
    """
    Handles the tag selection step for inventory.
    """
    query = update.callback_query
    await query.answer()

    if query.data == 'back':
        # Go back to the quantity selection step
        await query.edit_message_text(
            text="Choose a quantity:",
            reply_markup=Keyboards.get_quantities_keyboard()
        )
        return "QUANTITY"
    elif query.data == 'home':
        # Go back to the start menu
        await query.edit_message_text(
            text="Welcome! Choose a product:",
            reply_markup=Keyboards.get_products_keyboard()
        )
        return ConversationHandler.END
    else:
        # Save the selected tag and proceed to the confirmation step
        context.user_data['tag'] = query.data.replace('tag_', '')
        await query.edit_message_text(
            text=f"Confirm adding:\n"
                 f"Product: {context.user_data['product']}\n"
                 f"Size: {context.user_data['size']}\n"
                 f"Color: {context.user_data['color']}\n"
                 f"Quantity: {context.user_data['quantity']}\n"
                 f"Tag: {context.user_data['tag']}",
            reply_markup=Keyboards.get_confirmation_keyboard()
        )
        return "CONFIRM"

async def handle_confirmation(update: Update, context: CallbackContext):
    """
    Handles the confirmation step for inventory.
    """
    query = update.callback_query
    await query.answer()

    if query.data == 'confirm_ok':
        # Save the inventory entry to the database
        db.add_inventory(
            product_id=Config.PRODUCTS.index(context.user_data['product']),
            size=context.user_data['size'],
            color=context.user_data['color'],
            quantity=context.user_data['quantity'],
            tag=context.user_data['tag']
        )
        await query.edit_message_text(
            text="Inventory updated successfully!"
        )
        return ConversationHandler.END
    elif query.data == 'confirm_cancel':
        # Cancel the operation
        await query.edit_message_text(
            text="Operation cancelled."
        )
        return ConversationHandler.END
    elif query.data == 'back':
        # Go back to the tag selection step
        await query.edit_message_text(
            text="Choose a tag:",
            reply_markup=Keyboards.get_tags_keyboard()
        )
        return "TAG"
    elif query.data == 'home':
        # Go back to the start menu
        await query.edit_message_text(
            text="Welcome! Choose a product:",
            reply_markup=Keyboards.get_products_keyboard()
        )
        return ConversationHandler.END