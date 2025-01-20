# telegram_bot_inventory/main.py
import asyncio
import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ConversationHandler
from config.config import Config
from database.models import init_db
from handlers.start_handler import start_handler
from handlers.product_handler import handle_product_selection, handle_action_selection, cancel
from handlers.inventory_handler import (
    handle_size_selection as inventory_handle_size_selection,
    handle_color_selection as inventory_handle_color_selection,
    handle_quantity_selection as inventory_handle_quantity_selection,
    handle_tag_selection as inventory_handle_tag_selection,
    handle_confirmation as inventory_handle_confirmation
)
from handlers.stock_handler import (
    handle_size_selection as stock_handle_size_selection,
    handle_color_selection as stock_handle_color_selection
)

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define conversation states
PRODUCT, ACTION = range(2)
SIZE, COLOR, QUANTITY, TAG, CONFIRM = range(2, 7)

async def main():
    # Initialize database
    init_db()
    
    # Initialize bot
    application = Application.builder().token(Config.BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(start_handler)

    # Add conversation handler for product and inventory/stock flows
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_handler)],
        states={
            PRODUCT: [CallbackQueryHandler(handle_product_selection)],
            ACTION: [CallbackQueryHandler(handle_action_selection)],
            SIZE: [
                CallbackQueryHandler(inventory_handle_size_selection, pattern='^inventory$'),
                CallbackQueryHandler(stock_handle_size_selection, pattern='^stock$')
            ],
            COLOR: [
                CallbackQueryHandler(inventory_handle_color_selection, pattern='^inventory$'),
                CallbackQueryHandler(stock_handle_color_selection, pattern='^stock$')
            ],
            QUANTITY: [CallbackQueryHandler(inventory_handle_quantity_selection)],
            TAG: [CallbackQueryHandler(inventory_handle_tag_selection)],
            CONFIRM: [CallbackQueryHandler(inventory_handle_confirmation)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(conv_handler)
    
    # Start bot
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())