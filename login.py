import pymysql as mc
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

# connessione al database
myconn= mc.connect(host="localhost",user = "root", passwd="",database="tg_bot")

# func handler
async def start(update: Update, context: CallbackContext):
    # inserire logging start
    await update.message.reply_text("Ciao, vi servirò fino alla fine \nDigita il comando /login per utilizzare il bot!\nSe necessario utilizza il comando /cancel per ritornare a questa schermata!")
    
async def login(update: Update, context:CallbackContext):
    # verifica whitelist da db
    cur=myconn.cursor() 
    cur.execute("select * from whitelist")
    whitelist=[i[0] for i in cur.fetchall()]
    cur.close()


    # inserire logging login
    if update.message.from_user.username not in whitelist:
        await update.message.reply_text(
            "inserisci la password d'accesso: ")
        return LOGIN_CHECK
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,text=
            "Sei già loggato nel sistema, accedi al menù!")
        return ConversationHandler.END

async def login_check(update: Update, context:CallbackContext):

    if update.message.text=="fromfarmtofork":
        # insert username nella whitelist del db
        cur=myconn.cursor()
        cur.execute(f"INSERT INTO `whitelist` (`username`) VALUES ('{update.message.from_user.username}')")
        cur.close()

        await context.bot.send_message(chat_id=update.effective_chat.id,text=
            "Password corretta!\n ora puoi accedere alle funzioni del bot!")
        await context.bot.send_message(chat_id=update.effective_chat.id,text=
        "il menù rimane da aggiungere")
        return ConversationHandler.END
    else:
        await update.message.reply_text(
        "riprova a inserire la password:")
        return LOGIN_CHECK

async def menu(update: Update, context:CallbackContext):
    # inserire logging menu
    return 


async def cancel(update: Update, context: CallbackContext) -> int:
    # inserire logging cancel
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