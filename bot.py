from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import config

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
        await query.edit_message_text("🔧 You selected 'Add Product'.")
        # Future: Trigger add_product function here
    elif query.data == 'check_inventory':
        await query.edit_message_text("📊 Checking Inventory...")
        # Future: Trigger inventory display
    elif query.data == 'update_stock':
        await query.edit_message_text("⚙️ Update Stock selected.")
        # Future: Trigger update_stock flow

# Main Function - Register Handlers
def main():
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start))

    # Callback Query Handler
    app.add_handler(CallbackQueryHandler(button_click))

    print("Bot running... 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()