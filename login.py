import logging
from warnings import filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CommandHandler, Updater, MessageHandler, filters, TypeHandler, ConversationHandler, Application

# first initialization
application = Application.builder().token("5303090973:AAFBaJq-r9NgbHQv4CDNWRkJuzRi0sE1Eb0").build()
"""updater = Updater(token="5303090973:AAFBaJq-r9NgbHQv4CDNWRkJuzRi0sE1Eb0", use_context=True)"""
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
# app func
LOGIN, LOGIN_CHECK, MENU=range(3)

# func handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Ciao, vi servirò fino alla fine \nDigita il comando /login per utilizzare il bot!\nSe necessario utilizza il comando /cancel per ritornare a questa schermata!")

async def login(update: Update, context:CallbackContext):
    await update.message.reply_text(
        "inserisci la password d'accesso: ")
    return LOGIN_CHECK

async def login_check(update: Update, context:CallbackContext):
    if update.message.text=="fromfarmtofork":
        await update.message.reply_text(
            "Password corretta!\n ora puoi accedere alle funzioni del bot!")
        return MENU
    else:
        await update.message.reply_text(
        "riprova a inserire la password:")
        return LOGIN_CHECK

async def menu(update: Update, context:CallbackContext):
    await update.message.reply_text(
        "il menù rimane da aggiungere")
    return ConversationHandler.END


async def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Ritorni alla schermata iniziale!")
    return ConversationHandler.END

# main
def main():
    # handler
    start_handler = CommandHandler('start', start)
    login_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("login", login)],
        states={
            LOGIN_CHECK: [MessageHandler(filters.TEXT,login_check)],
            MENU: [MessageHandler(filters.TEXT,menu)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    # dispatcher add handler
    application.add_handler(start_handler)
    application.add_handler(login_conv_handler)
    # start
    application.run_polling(close_loop=True)

if __name__ == '__main__':
    main()