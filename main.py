import os
from typing import Final

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (Application, CallbackContext, CommandHandler,
                          ContextTypes, MessageHandler, Updater, filters)

load_dotenv()

TOKEN: Final[str] = os.getenv('TOKEN')
BOT_USERNAME: Final[str] = os.getenv('BOT_USERNAME')

async def start_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Greetings, Earthling! I am Lemmon, your friendly neighborhood bot! 🍋')

async def help_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Need help? Just type something, and I\'ll do my best to sound like I know what I\'m talking about! 🤖')

async def custom_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command. Much like a secret handshake, but with less handshaking and more typing. 🤷‍♂️')

def handle_responses(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there! 👋 How’s life treating you?'

    if 'how are you' in processed:
        return 'I’m doing great, thanks for asking! Just here, making the world a bit more... robotic. 🤖'

    if 'i love python' in processed:
        return 'Python, you say? 🐍 That’s my favorite language! We’re practically besties.'

    return 'I’m not sure what you mean, but I’m here to help! Or at least make you laugh. 😄'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'user ({update.message.chat.id}) in {message_type}')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_responses(new_text)
        else:
            return
    else:
        response: str = handle_responses(text)
    
    print('Bot: ', response)

    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)
