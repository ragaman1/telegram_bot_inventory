# bot.py
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import config
from commands import start, button_click, handle_message
from database import initialize_database

# Initialize the database
initialize_database()

# Main Function - Register Handlers
def main():
    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()

    # Command Handlers
    app.add_handler(CommandHandler("start", start))

    # Callback Query Handler
    app.add_handler(CallbackQueryHandler(button_click))

    # Message Handler for User Input
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running... 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()