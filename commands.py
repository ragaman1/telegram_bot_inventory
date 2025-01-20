# commands.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from inventory import add_new_product, get_inventory
from utils import validate_quantity, format_inventory

# Start Command - Display Inline Buttons
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📦 Add Product", callback_data='add_product')],
        [InlineKeyboardButton("📊 Check Inventory", callback_data='check_inventory')],
        [InlineKeyboardButton("⚙️ Update Stock", callback_data='update_stock')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome to Inventory Manager Bot! 👋\n\nChoose an option below:",
        reply_markup=reply_markup
    )

# Callback Handler for Inline Button Press
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'add_product':
        await query.edit_message_text("📝 Please enter the product name:")
        context.user_data["step"] = "awaiting_product_name"  # Track the current step
    elif query.data == 'check_inventory':
        products = get_inventory()
        response = format_inventory(products)
        await query.edit_message_text(response)
    elif query.data == 'update_stock':
        await query.edit_message_text("⚙️ Update Stock selected.")
        # Future: Trigger update_stock flow

# Handle User Input for Adding Product
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    text = update.message.text

    if user_data.get("step") == "awaiting_product_name":
        # Save product name and ask for size
        user_data["product_name"] = text
        user_data["step"] = "awaiting_product_size"
        await update.message.reply_text("📏 Please enter the product size:")
    elif user_data.get("step") == "awaiting_product_size":
        # Save product size and ask for color
        user_data["product_size"] = text
        user_data["step"] = "awaiting_product_color"
        await update.message.reply_text("🎨 Please enter the product color:")
    elif user_data.get("step") == "awaiting_product_color":
        # Save product color and ask for quantity
        user_data["product_color"] = text
        user_data["step"] = "awaiting_product_quantity"
        await update.message.reply_text("🔢 Please enter the product quantity:")
    elif user_data.get("step") == "awaiting_product_quantity":
        # Save product quantity and add to database
        try:
            quantity = int(text)
            if not validate_quantity(quantity):
                await update.message.reply_text("❌ Quantity must be a positive number. Please try again.")
                return

            # Add the product to the database
            success = add_new_product(
                name=user_data["product_name"],
                size=user_data["product_size"],
                color=user_data["product_color"],
                quantity=quantity
            )

            if success:
                # Clear user data
                user_data.clear()
                await update.message.reply_text("✅ Product added successfully!")
            else:
                await update.message.reply_text("❌ Failed to add product. Please try again.")
        except ValueError:
            await update.message.reply_text("❌ Invalid quantity. Please enter a number.")