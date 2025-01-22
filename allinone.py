from datetime import datetime
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
    SELECTING_PLACE,  # New state
    CONFIRMING_ACTION
) = range(8)

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

place_keyboard = [
    ["Place 1", "Place 2"],
    ["Home", "Back"]
]

confirmation_keyboard = [
    ["OK", "Cancel"],
    ["Home", "Back"]
]


def initialize_database():
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()

    # Create the inventory table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT NOT NULL,
            size TEXT NOT NULL,
            color TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            place TEXT NOT NULL,  -- New column
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()



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
        # Fetch stock and last_updated timestamp from database
        stock, last_updated = get_stock(
            context.user_data['product'],
            context.user_data['size'],
            context.user_data['color'],
            context.user_data['place']
        )
        await update.message.reply_text(
            f"Current stock: {stock} units\n"
            f"Last Updated: {last_updated}\n"
            "Select 'Home' to start over",
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
        "Select the place:",
        reply_markup=ReplyKeyboardMarkup(place_keyboard, one_time_keyboard=True)
    )
    return SELECTING_PLACE

async def place_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle place selection."""
    text = update.message.text
    context.user_data['place'] = text
    
    await update.message.reply_text(
        f"You want to {context.user_data['operation']} {context.user_data['quantity']} units of:\n"
        f"Product: {context.user_data['product']}\n"
        f"Size: {context.user_data['size']}\n"
        f"Color: {context.user_data['color']}\n"
        f"Place: {context.user_data['place']}\n"
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
                context.user_data['place'],  # Include place
                context.user_data['operation']
            )
            # Fetch the updated stock and last_updated timestamp
            stock, last_updated = get_stock(
                context.user_data['product'],
                context.user_data['size'],
                context.user_data['color'],
                context.user_data['place']  # Include place
            )
            await update.message.reply_text(
                f"Inventory updated successfully!\n"
                f"New stock: {stock} units\n"
                f"Place: {context.user_data['place']}\n"
                f"Last Updated: {last_updated}",
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
def get_stock(product, size, color, place):
    """Fetch stock and last updated timestamp from database."""
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Query the database for the stock and last_updated timestamp
    cursor.execute('''
    SELECT quantity, last_updated FROM inventory
    WHERE product = ? AND size = ? AND color = ? AND place = ?
    ''', (product, size, color, place))
    
    result = cursor.fetchone()
    conn.close()
    
    # Return (quantity, last_updated) if found, otherwise (0, None)
    return result if result else (0, None)

def update_inventory(product, size, color, quantity, place, operation):
    """Update inventory and last_updated timestamp in database."""
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    # Fetch current stock
    current_stock, _ = get_stock(product, size, color, place)
    
    if operation == "Add":
        new_stock = current_stock + quantity
    elif operation == "Remove":
        new_stock = max(0, current_stock - quantity)  # Ensure stock doesn't go below 0
    
    # Update or insert the new stock value and last_updated timestamp
    cursor.execute('''
    INSERT OR REPLACE INTO inventory (product, size, color, quantity, place, last_updated)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (product, size, color, new_stock, place, datetime.now()))
    
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
            SELECTING_PLACE: [  # New state
                MessageHandler(
                    filters.Regex("^(Place 1|Place 2)$"), 
                    place_choice
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
    initialize_database()
    main()

#FIXME: 
'''
2025-01-22 08:02:50,896 - __main__ - WARNING - Update "Update(message=Message(channel_chat_created=False, chat=Chat(first_name='Amir', id=2007423925, type=<ChatType.PRIVATE>, username='ragaman1'),
 date=datetime.datetime(2025, 1, 22, 13, 2, 50, tzinfo=datetime.timezone.utc), delete_chat_photo=False, from_user=User(first_name='Amir', id=2007423925, is_bot=False, language_code='en',
   username='ragaman1'), group_chat_created=False, message_id=1271, supergroup_chat_created=False, text='Color 4'), update_id=91167737)" caused error "'place'"'''