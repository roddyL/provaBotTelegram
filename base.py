from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

updater = Updater("5303090973:AAFBaJq-r9NgbHQv4CDNWRkJuzRi0sE1Eb0",
                  use_context=True)
  
  
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Fanculo Loris e Alberto!!")

def help(update: Update, context: CallbackContext):
    update.message.reply_text("shorturl.at/BDHI8")

def main():
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    updater.start_polling()
    updater.idle()  

if __name__ == '__main__':
    main()