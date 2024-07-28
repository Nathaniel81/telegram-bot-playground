import os
from typing import Final

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from telegram.ext import (Application, CallbackContext, CommandHandler,
                          ContextTypes, MessageHandler, CallbackQueryHandler, Updater, filters)

load_dotenv()

TOKEN: Final[str] = os.getenv('TOKEN')
BOT_USERNAME: Final[str] = os.getenv('BOT_USERNAME')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton('Help', callback_data='help')],
        [InlineKeyboardButton('Custom Command', callback_data='custom')],
        [InlineKeyboardButton('Remove Keyboard', callback_data='remove_keyboard')]
    ]
    
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(
        'Greetings, Earthling! I am Lemmon, your friendly neighborhood bot! 🍋',
        reply_markup=keyboard
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Need help? Just type something, and I\'ll do my best to sound like I know what I\'m talking about! 🤖')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command. Much like a secret handshake, but with less handshaking and more typing. 🤷‍♂️')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    response_text = None

    if data == 'help':
        response_text = 'You clicked "Help"! Here\'s some help for you. 🤖'
    elif data == 'custom':
        response_text = 'You clicked "Custom Command"! Here\'s your custom response. 🎩'
    elif data == 'remove_keyboard':
        response_text = 'Removing keyboard... 👋'
    
    if response_text:
        if query.message:
            await query.message.reply_text(response_text)
        else:
            await context.bot.send_message(chat_id=query.from_user.id, text=response_text)
        
        if data == 'remove_keyboard':
            if query.message:
                await query.message.reply_text('Keyboard removed.', reply_markup=ReplyKeyboardRemove())
            else:
                await context.bot.send_message(chat_id=query.from_user.id, text='Keyboard removed.', reply_markup=ReplyKeyboardRemove())

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CallbackQueryHandler(button_callback))

    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)
