from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
import telegram.ext.messagehandler
from telegram.ext.filters import Filters

updater = Updater("5303090973:AAFBaJq-r9NgbHQv4CDNWRkJuzRi0sE1Eb0",
                  use_context=True)
  
  
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Fanculo Loris e Alberto!!")

def help(update: Update, context: CallbackContext):
    update.message.reply_text("shorturl.at/BDHI8")

def handle_message(bot, update):
    text = update.message.text
    if text == 'hello':
        update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))

def main():
    dp = updater.dispatcher
    dp.add_handler(CommandHandler(["start","ciao"], start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler()
    updater.start_polling()
    updater.idle()  

if __name__ == '__main__':
    main()