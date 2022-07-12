import logging
from warnings import filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CommandHandler, Updater, MessageHandler, Filters, TypeHandler, ConversationHandler

# first initialization
updater = Updater(token='5303090973:AAFBaJq-r9NgbHQv4CDNWRkJuzRi0sE1Eb0', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
# app func


# func handler
def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ciao, vi servirò fino alla fine")

def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def exit(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ciao, me ne vado")
    updater.stop()

def buttonsInLinea(update: Update, context: CallbackContext):
    options = []
    options.append(InlineKeyboardButton(text='scelta 1', callback_data='1'))
    options.append(InlineKeyboardButton(text='scelta 2', callback_data='2'))
    options.append(InlineKeyboardButton(text='scelta 3', callback_data='3'))
    options.append(InlineKeyboardButton(text='scelta 4', callback_data='4'))
    reply_markup = InlineKeyboardMarkup([options])
    context.bot.send_message(chat_id=update.effective_chat.id, text='Clicca una delle scelte', reply_markup=reply_markup)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"hai scelto l'opzione numero{update.callback_query.data}")
    

def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Non c'è alcun comando scritto così")


# main
def main():
    # handler
    start_handler = CommandHandler('start', start, filters=~Filters.update.edited_message)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    buttonsInLinea_handler = CommandHandler('buttonsInLinea', buttonsInLinea, filters=~Filters.update.edited_message)
    unknown_handler = MessageHandler(Filters.command, unknown)


    # dispatcher add handler
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(buttonsInLinea_handler)
    dispatcher.add_handler(unknown_handler)

    # start
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()