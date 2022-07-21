import pymysql as mc
import logging
from typing import Union, List
from warnings import filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CommandHandler, Updater, MessageHandler, filters, TypeHandler, ConversationHandler, Application, CallbackQueryHandler

# first initialization
application = Application.builder().token("5303090973:AAFBaJq-r9NgbHQv4CDNWRkJuzRi0sE1Eb0").build()

# creazione del logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# variabili conversation handler
LOGIN, LOGIN_CHECK, MENU, BUTTON=range(4)

# funzioni

def build_menu(
    buttons: List[InlineKeyboardButton],
    n_cols: int,
    header_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None,
    footer_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None
) -> List[List[InlineKeyboardButton]]:
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons if isinstance(header_buttons, list) else [header_buttons])
    if footer_buttons:
        menu.append(footer_buttons if isinstance(footer_buttons, list) else [footer_buttons])
    return menu

def insert_whitelist(username):
    with mc.connect(host="localhost",user = "root", passwd="",database="tg_bot",cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(f"INSERT INTO `whitelist` (`username`,`dt_lastLogin`) VALUES ('{username}',CURRENT_TIMESTAMP)")
            __myconn.commit()

def check_whitelist(already_logged=False):
    if already_logged:
        logged=0
    else:
        logged=1
    with mc.connect(host="localhost",user = "root", passwd="",database="tg_bot",cursorclass=mc.cursors.DictCursor) as __myconn:
        # update whitelist da database
        with __myconn.cursor() as cur: 
            cur.execute(f"select * from whitelist where is_logged={logged}")
            whitelist=[i["username"] for i in cur.fetchall()]

    return whitelist

def update_session(username):
    with mc.connect(host="localhost",user = "root", passwd="",database="tg_bot",cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(f"UPDATE `whitelist` SET is_logged=1, dt_lastLogin=CURRENT_TIMESTAMP WHERE username='{username}'")
            __myconn.commit()

def logout(username):
    with mc.connect(host="localhost",user = "root", passwd="",database="tg_bot",cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(f"UPDATE `whitelist` SET is_logged=0 WHERE username='{username}'")
            __myconn.commit()

def menu_interface_main(input=None):
    keyboard = [
                InlineKeyboardButton("prenotazioni 📅", callback_data='m1_1'),
                InlineKeyboardButton("", callback_data='m1_2'),
                InlineKeyboardButton("Option 3", callback_data='m1_3')
        ]
    reply_markup = InlineKeyboardMarkup(build_menu(keyboard,n_cols=3))
    text_reply=f""
    return text_reply,reply_markup

def menu_interface_m1_1(input):
    keyboard = [
                InlineKeyboardButton("nuova prenotazione", callback_data='m2_1'),
                InlineKeyboardButton("cancella prenotazione", callback_data='m2_2'),
                InlineKeyboardButton("le mie prenotazioni", callback_data='m2_3')
        ]
    reply_markup = InlineKeyboardMarkup(build_menu(keyboard,n_cols=3))
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
    username=update.message.from_user.username
    passInserita=update.message.text
    messageId=update.message.message_id
    # cancellazione messaggi
    await application.bot.delete_message(chat_id=update.message.chat_id, message_id=messageId)
    # await application.bot.delete_message(chat_id=update.message.chat_id, message_id=messageId-1)
    
    if passInserita=="fromfarmtofork":
        if username not in check_whitelist(True) and username not in check_whitelist():
            logger.info("Log in dell'utente \'%s\' riuscito. Registrazione in corso.", username)
            insert_whitelist(username)
        else:
            update_session(username)
            logger.info("Log in dell'utente \'%s\' riuscito. Update della sessione.", username)
        await context.bot.send_message(chat_id=update.effective_chat.id,text=
            "Password corretta!\n ora puoi accedere alle funzioni del bot!\nDigita il comando /menu per accedere al menu")
        return MENU
    else:
        logger.info("Log in dell'utente \'%s\' non riuscito. Password usata: %s", username, passInserita)
        await update.message.reply_text(
        "riprova a inserire la password:")
        return LOGIN_CHECK

async def menu(update: Update, context:CallbackContext):
    username=update.message.from_user.username
    
    # se è un utente nuovo fa la registrazione
    if username not in check_whitelist():
        await context.bot.send_message(chat_id=update.effective_chat.id,text=
            "La sessione è scaduta, ripassa per il /login !")
        return ConversationHandler.END
    else:
        update_session(username)
        interfaccia=menu_interface_main()
        await update.message.reply_text('Please choose:', reply_markup=interfaccia[1])
        return BUTTON

async def button(update: Update, context: CallbackContext) -> None:
    username=update.callback_query.from_user.username
    
    if username not in check_whitelist():
        await context.bot.send_message(chat_id=update.effective_chat.id,text=
            "La sessione è scaduta, ripassa per il /login !")
        return ConversationHandler.END
    else:
        update_session(username)
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


async def fallback(update: Update, context: CallbackContext) -> int:
    username=update.message.from_user.username
    if update.message.text=="/cancel":
        logger.info("L'utente \'%s\' ha cancellato il log in.",username)
        await update.message.reply_text(
            "Ritorni alla schermata iniziale!")
    else:
        logout(username)
        logger.info("L'utente \'%s\' ha effettuato il logout.",username)
        await update.message.reply_text(
            "Logout effettuato!")

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
        fallbacks=[CommandHandler(["cancel","logout"], fallback)]
    )

    # dispatcher add handler
    application.add_handler(start_handler)
    application.add_handler(login_conv_handler)


    # start
    application.run_polling(close_loop=True)

if __name__ == '__main__':
    main()