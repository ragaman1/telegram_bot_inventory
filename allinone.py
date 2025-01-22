from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from telegram.ext import Application, CommandHandler, ConversationHandler
import logging
import sqlite3

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# States
(
    SELECTING_PRODUCT,
    SELECTING_ACTION,
    SELECTING_OPERATION,
    SELECTING_SIZE,
    SELECTING_COLOR,
    SELECTING_QUANTITY,
    CONFIRMING_ACTION
) = range(7)

# Keyboard layouts
product_keyboard = [
    ["Product 1", "Product 2"],
]

action_keyboard = [
    ["Inventory", "Stock"],
    ["Home", "Back"]
]

inventory_keyboard = [
    ["Add", "Remove"],
    ["Home", "Back"]
]

size_keyboard = [
    ["Size 1", "Size 2"],
    ["Size 3", "Size 4"],
    ["Home", "Back"]
]

color_keyboard = [
    ["Color 1", "Color 2", "Color 3"],
    ["Color 4", "Color 5"],
    ["Home", "Back"]
]

quantity_keyboard = [
    ["1", "2", "3", "4"],
    ["Home", "Back"]
]

confirmation_keyboard = [
    ["OK", "Cancel"],
    ["Home", "Back"]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user to choose product."""
    context.user_data.clear()
    await update.message.reply_text(
        "Welcome to Inventory Management Bot!\n"
        "Please select a product:",
        reply_markup=ReplyKeyboardMarkup(product_keyboard, one_time_keyboard=True)
    )
    return SELECTING_PRODUCT

async def product_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle product selection."""
    text = update.message.text
    context.user_data['product'] = text
    
    await update.message.reply_text(
        f"You selected {text}.\n"
        "What would you like to do?",
        reply_markup=ReplyKeyboardMarkup(action_keyboard, one_time_keyboard=True)
    )
    return SELECTING_ACTION

async def action_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle action selection (Inventory/Stock)."""
    text = update.message.text
    context.user_data['action'] = text
    
    if text == "Inventory":
        await update.message.reply_text(
            "Choose operation:",
            reply_markup=ReplyKeyboardMarkup(inventory_keyboard, one_time_keyboard=True)
        )
        return SELECTING_OPERATION
    else:  # Stock
        await update.message.reply_text(
            "Select size to check stock:",
            reply_markup=ReplyKeyboardMarkup(size_keyboard, one_time_keyboard=True)
        )
        return SELECTING_SIZE

async def operation_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle operation selection (Add/Remove)."""
    text = update.message.text
    context.user_data['operation'] = text
    
    await update.message.reply_text(
        "Select size:",
        reply_markup=ReplyKeyboardMarkup(size_keyboard, one_time_keyboard=True)
    )
    return SELECTING_SIZE

async def size_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle size selection."""
    text = update.message.text
    context.user_data['size'] = text
    
    await update.message.reply_text(
        "Select color:",
        reply_markup=ReplyKeyboardMarkup(color_keyboard, one_time_keyboard=True)
    )
    return SELECTING_COLOR

async def color_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle color selection."""
    text = update.message.text
    context.user_data['color'] = text
    
    if context.user_data.get('action') == 'Stock':
        # Fetch stock from database
        stock = get_stock(
            context.user_data['product'],
            context.user_data['size'],
            context.user_data['color']
        )
        await update.message.reply_text(
            f"Current stock: {stock} units\n"
            "Select'Home' to start over",
            reply_markup=ReplyKeyboardMarkup([["Home", "Back"]], one_time_keyboard=True)
        )
        return SELECTING_SIZE
    else:
        await update.message.reply_text(
            "Select quantity:",
            reply_markup=ReplyKeyboardMarkup(quantity_keyboard, one_time_keyboard=True)
        )
        return SELECTING_QUANTITY

async def quantity_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle quantity selection."""
    text = update.message.text
    context.user_data['quantity'] = int(text)
    
    await update.message.reply_text(
        f"You want to {context.user_data['operation']} {text} units of:\n"
        f"Product: {context.user_data['product']}\n"
        f"Size: {context.user_data['size']}\n"
        f"Color: {context.user_data['color']}\n"
        "Is this correct?",
        reply_markup=ReplyKeyboardMarkup(confirmation_keyboard, one_time_keyboard=True)
    )
    return CONFIRMING_ACTION

async def confirm_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle final confirmation."""
    text = update.message.text
    
    if text == "OK":
        # Update database
        try:
            update_inventory(
                context.user_data['product'],
                context.user_data['size'],
                context.user_data['color'],
                context.user_data['quantity'],
                context.user_data['operation']
            )
            await update.message.reply_text(
                "Inventory updated successfully!",
                reply_markup=ReplyKeyboardMarkup(product_keyboard, one_time_keyboard=True)
            )
        except Exception as e:
            await update.message.reply_text(
                f"Error updating inventory: {str(e)}",
                reply_markup=ReplyKeyboardMarkup(product_keyboard, one_time_keyboard=True)
            )
    else:  # Cancel
        await update.message.reply_text(
            "Operation cancelled.",
            reply_markup=ReplyKeyboardMarkup(product_keyboard, one_time_keyboard=True)
        )
    
    context.user_data.clear()
    return SELECTING_PRODUCT

async def back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle 'Back' button."""
    current_state = context.user_data.get('state', SELECTING_PRODUCT)
    
    # Remove the last entered data
    if 'quantity' in context.user_data:
        del context.user_data['quantity']
        return await color_choice(update, context)
    elif 'color' in context.user_data:
        del context.user_data['color']
        return await size_choice(update, context)
    elif 'size' in context.user_data:
        del context.user_data['size']
        return await action_choice(update, context)
    elif 'action' in context.user_data:
        del context.user_data['action']
        return await product_choice(update, context)
    else:
        return await start(update, context)

async def back_to_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle 'Home' button."""
    return await start(update, context)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel conversation."""
    await update.message.reply_text(
        "Operation cancelled. Send /start to begin again.",
        reply_markup=ReplyKeyboardMarkup(product_keyboard, one_time_keyboard=True)
    )
    context.user_data.clear()
    return ConversationHandler.END

# Database functions (you need to implement these)
def get_stock(product, size, color):
    """Fetch stock from database."""
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Query the database for the stock of the given product, size, and color
    cursor.execute('''
    SELECT quantity FROM inventory
    WHERE product = ? AND size = ? AND color = ?
    ''', (product, size, color))
    
    result = cursor.fetchone()
    conn.close()
    
    # Return 0 if no record is found, otherwise return the quantity
    return result[0] if result else 0

def update_inventory(product, size, color, quantity, operation):
    """Update inventory in database."""
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Fetch current stock
    current_stock = get_stock(product, size, color)
    
    if operation == "Add":
        new_stock = current_stock + quantity
    elif operation == "Remove":
        new_stock = max(0, current_stock - quantity)  # Ensure stock doesn't go below 0
    
    # Update or insert the new stock value
    cursor.execute('''
    INSERT OR REPLACE INTO inventory (product, size, color, quantity)
    VALUES (?, ?, ?, ?)
    ''', (product, size, color, new_stock))
    
    conn.commit()
    conn.close()

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6977044112:AAHw8PfnzDPtBST1Zz8YhWRdpt4zi9fZqX0").build()

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECTING_PRODUCT: [
                MessageHandler(
                    filters.Regex("^(Product 1|Product 2)$"), 
                    product_choice
                )
            ],
            SELECTING_ACTION: [
                MessageHandler(
                    filters.Regex("^(Inventory|Stock)$"), 
                    action_choice
                ),
                MessageHandler(filters.Regex("^Back$"), back_handler),
                MessageHandler(filters.Regex("^Home$"), back_to_start)
            ],
            SELECTING_OPERATION: [
                MessageHandler(
                    filters.Regex("^(Add|Remove)$"), 
                    operation_choice
                ),
                MessageHandler(filters.Regex("^Back$"), back_handler),
                MessageHandler(filters.Regex("^Home$"), back_to_start)
            ],
            SELECTING_SIZE: [
                MessageHandler(
                    filters.Regex("^Size [1-4]$"), 
                    size_choice
                ),
                MessageHandler(filters.Regex("^Back$"), back_handler),
                MessageHandler(filters.Regex("^Home$"), back_to_start)
            ],
            SELECTING_COLOR: [
                MessageHandler(
                    filters.Regex("^Color [1-5]$"), 
                    color_choice
                ),
                MessageHandler(filters.Regex("^Back$"), back_handler),
                MessageHandler(filters.Regex("^Home$"), back_to_start)
            ],
            SELECTING_QUANTITY: [
                MessageHandler(
                    filters.Regex("^[1-4]$"), 
                    quantity_choice
                ),
                MessageHandler(filters.Regex("^Back$"), back_handler),
                MessageHandler(filters.Regex("^Home$"), back_to_start)
            ],
            CONFIRMING_ACTION: [
                MessageHandler(
                    filters.Regex("^(OK|Cancel)$"), 
                    confirm_action
                ),
                MessageHandler(filters.Regex("^Back$"), back_handler),
                MessageHandler(filters.Regex("^Home$"), back_to_start)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            MessageHandler(filters.Regex("^Cancel$"), cancel)
        ],
    )

    # Add the conversation handler to the application
    application.add_handler(conv_handler)

    # Log all errors
    application.add_error_handler(error_handler)

    # Run the bot until the user presses Ctrl-C
    print("Bot started...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

# Error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    # Send message to user
    if update.effective_message:
        await update.effective_message.reply_text(
            "Sorry, something went wrong. Please try again or start over with /start"
        )

if __name__ == '__main__':
    main()