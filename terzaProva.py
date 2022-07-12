import logging
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater
from telegram.ext.filters import Filters

updater = Updater(token='5303090973:AAFBaJq-r9NgbHQv4CDNWRkJuzRi0sE1Eb0', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ciao, vi servirò fino alla fine")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler,filter=Filters._UpdateType.edited_message)

updater.start_polling()