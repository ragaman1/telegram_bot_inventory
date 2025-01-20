from telegram.ext import CommandHandler
from keyboards.keyboards import Keyboards

async def start(update, context):
    keyboard = Keyboards.get_products_keyboard()
    await update.message.reply_text(
        'Welcome to Inventory Management Bot!\nPlease select a product:',
        reply_markup=keyboard
    )

start_handler = CommandHandler('start', start)