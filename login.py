import pymysql as mc
import logging
from warnings import filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import CallbackContext, CommandHandler, Updater, MessageHandler, filters, TypeHandler, ConversationHandler, Application, CallbackQueryHandler

# first initialization
application = Application.builder().token("5303090973:AAFBaJq-r9NgbHQv4CDNWRkJuzRi0sE1Eb0").build()
"""updater = Updater(token="5303090973:AAFBaJq-r9NgbHQv4CDNWRkJuzRi0sE1Eb0", use_context=True)"""
# creazione del logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
# app func
LOGIN, LOGIN_CHECK, MENU, BUTTON=range(4)

# funzioni

def check_whitelist():
    with mc.connect(host="localhost",user = "root", passwd="",database="tg_bot",cursorclass=mc.cursors.DictCursor) as __myconn:
        # update whitelist da database
        cur=__myconn.cursor() 
        cur.execute("select * from whitelist where is_logged=1")
        whitelist=[i["username"] for i in cur.fetchall()]
        cur.close()
    return whitelist

def menu_interface_main(input=None):
    keyboard = [
            [
                InlineKeyboardButton("Option 1", callback_data='m1_1'),
                InlineKeyboardButton("Option 2", callback_data='m1_2'),
            ],
            [   InlineKeyboardButton("Option 3", callback_data='m1_3')
            ],
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text_reply=f""
    return text_reply,reply_markup

def menu_interface_m1_1(input):
    keyboard = [
            [
                InlineKeyboardButton("Scelta 1 ", callback_data='m2_1'),
                InlineKeyboardButton("Scelta 2", callback_data='m2_2'),
            ],
            [   InlineKeyboardButton("Scelta 3", callback_data='m2_3')
            ],
        ]
    reply_markup=InlineKeyboardMarkup(keyboard)
    text_reply=f"Hai scelto: {input} ora scegli ancora: "
    return text_reply, reply_markup

def menu_interface_m2_1(input):
    reply_markup=None
    text_reply=f"Hai scelto: {input} ora basta, hai finito girare"
    return text_reply, reply_markup

# func handler
async def start(update: Update, context: CallbackContext):
    logger.info("Utente \'%s\' ha avviato la conversazione %s.",update.message.from_user.username, update.message.chat_id)
    # inserire logging start
    await update.message.reply_text("Ciao, vi servirò fino alla fine \nDigita il comando /login per utilizzare il bot!\nSe necessario utilizza il comando /cancel per ritornare a questa schermata!")
    
async def login(update: Update, context:CallbackContext):
    # se è un utente nuovo fa la registrazione
    if update.message.from_user.username not in check_whitelist():
        logger.info("Utente \'%s\' sta cercando di effettuare il log in.", update.message.from_user.username)
        await update.message.reply_text(
            "inserisci la password d'accesso: ")
        return LOGIN_CHECK
    # altrimenti rimanda al menù
    else:
        logger.info("Utente \'%s\' è gia registrato. Ha effettuato il log in.", update.message.from_user.username)
        await context.bot.send_message(chat_id=update.effective_chat.id,text=
            "Sei già loggato nel sistema, accedi al menù con /menu!")
        return MENU

async def login_check(update: Update, context:CallbackContext):
    # cancellazione messaggi
    passInserita=update.message.text
    messageId=update.message.message_id
    await application.bot.delete_message(chat_id=update.message.chat_id, message_id=messageId)
    # await application.bot.delete_message(chat_id=update.message.chat_id, message_id=messageId-1)
    
    if passInserita=="fromfarmtofork":
        logger.info("Log in dell'utente \'%s\' riuscito. Registrazione in corso.", update.message.from_user.username)
        # connessione al database
        with mc.connect(host="localhost",user = "root", passwd="",database="tg_bot") as __myconn:
            # insert username nella whitelist del db
            cur=__myconn.cursor()
            cur.execute(f"INSERT INTO `whitelist` (`username`) VALUES ('{update.message.from_user.username}')")
            __myconn.commit()
            cur.close()

        await context.bot.send_message(chat_id=update.effective_chat.id,text=
            "Password corretta!\n ora puoi accedere alle funzioni del bot!\nDigita il comando /menu per accedere al menu")
        return MENU
    else:
        logger.info("Log in dell'utente \'%s\' non riuscito. Password usata: %s", update.message.from_user.username, passInserita)
        await update.message.reply_text(
        "riprova a inserire la password:")
        return LOGIN_CHECK

async def menu(update: Update, context:CallbackContext):
    # se è un utente nuovo fa la registrazione
    if update.message.from_user.username not in check_whitelist():
        await context.bot.send_message(chat_id=update.effective_chat.id,text=
            "La sessione è scaduta, ripassa per il /login !")
        return ConversationHandler.END
    else:
        interfaccia=menu_interface_main()
        await update.message.reply_text('Please choose:', reply_markup=interfaccia[1])
        return BUTTON

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    if query.data=='m1_1':
        m1_1_interface=menu_interface_m1_1(query.data)
        await query.edit_message_text(text=m1_1_interface[0],reply_markup=m1_1_interface[1])
        return BUTTON
    elif query.data=='m2_1':
        m2_1_interface=menu_interface_m2_1(query.data)
        await query.edit_message_text(text=m2_1_interface[0],reply_markup=m2_1_interface[1])
        return MENU
    return MENU


async def cancel(update: Update, context: CallbackContext) -> int:
    logger.info("L'utente \'%s\' ha cancellato il log in.",update.message.from_user.username)
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
            MENU: [CommandHandler("menu", menu)],
            BUTTON: [CallbackQueryHandler(button)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    # button_handler=CallbackQueryHandler(button)

    # dispatcher add handler
    application.add_handler(start_handler)
    application.add_handler(login_conv_handler)
    # application.add_handler(button_handler)

    # start
    application.run_polling(close_loop=True)

if __name__ == '__main__':
    main()