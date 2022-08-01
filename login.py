# login.py

# import libraries
import pymysql as mc
import logging
import datetime
import calendar
from holidays import italy as italianHolidays
from typing import Union, List
from warnings import filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, filters, ConversationHandler, Application, CallbackQueryHandler

# first initialization
application = Application.builder().token("5303090973:AAFBaJq-r9NgbHQv4CDNWRkJuzRi0sE1Eb0").build()

# creazione del logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# variabili globali
month_enToIt={"January":"Gennaio","February":"Febbraio","March":"Marzo","April":"Aprile",
                "May":"Maggio","June":"Giugno","July":"Luglio","August":"Agosto","September":"Settembre",
                "October":"Ottobre","November":"Novembre","December":"Dicembre"}

# variabili conversation handler
LOGIN, LOGIN_CHECK, MENU, BUTTON=range(4)

# funzioni

def giorni_festivi(year: int, provincia: str) ->List[datetime.date]:
    """giorni_gestivi()

    Args:
        year (int): anno di cui visualizzare i giorni festivi
        provincia (str): codice della provincia che rileva giorni festivi locali  

    Returns:
        List[datetime.date]: lista di giorni festivi
    """
    festivi=[]
    for i, j in sorted(italianHolidays.Italy(subdiv=provincia,years=year).items()):
        if datetime.date.weekday(i)!=6:
            festivi.append(i)

    return festivi

def next_month(
    mese: int,
    anno: int
) -> str:
    """next_month()

    Args:
        mese (int): mese corrente
        anno (int): anno corrente

    Returns:
        str: prossimo mese formato 00/00/0000
    """
    if mese==12:
        prossimoMese=f"01/01/{anno+1}"
    else:
        prossimoMese=f"01/{mese+1}/{anno}"

    return prossimoMese

def previous_month(
    mese: int,
    anno: int
) -> str:
    """previous_month()

    Args:
        mese (int): mese corrente
        anno (int): anno corrente

    Returns:
        str: mese precedente formato 00/00/0000
    """
    if mese==1:
        mesePrecedente=f"01/12/{anno-1}"
    else:
        mesePrecedente=f"01/{mese-1}/{anno}"

    return mesePrecedente

def strike(
    text: str
) -> str:
    """strike()

    Args:
        text (str): testo da barrare

    Returns:
        str: testo barrato
    """
    result = ''
    for c in text:
        result += c + '\u0336'
    return result

def italics(
    text: str
) -> str:
    """italics()

    Args:
        text (str): testo da scrivere in corsivo

    Returns:
        str: testo in corsivo
    """
    result = ''
    for c in text:
        result+= '\x1B[3m' + c 
    return result

def bold(
    text: str
) -> str:
    """bold()

    Args:
        text (str): testo da scrivere in grassetto

    Returns:
        str: testo in grassetto
    """
    result = ''
    for c in text:
        result += '\033[1m' + c 
    return result

def dayInfo(
    day: datetime.date,
    holidays: List[datetime.date]=[]
)-> dict:
    """dayInfo()

    Args:
        day (datetime.date): giorno in cui estrapolare i giorni del mese
        holidays (List[datetime.date], optional): giorni festivi e ferie per l'azienda. Defaults to [].

    Returns:
        dict: {
            giorno (int): il numero del giorno,
            mese (str): il nome del mese in italiano,
            anno (int): l'anno in numero,
            lista_giorni (list[int]): giorni del mese da visualizzare, disponibili 🟩 e non disponibili ❌
        }
    """

    holidays=list(set(giorni_festivi(day.year,"PD"))|set(holidays))
    query_uffici_pieni=""
    giorni_uffici_pieni=[]
    giorni=[]
    for i in calendar.monthcalendar(day.year,day.month):
        for j in i:
            if j==0:
                giorni.append(" ")
            elif datetime.date(day.year, day.month, j) in holidays+giorni_uffici_pieni or i[-1]==j or i[-2]==j or (day.year==datetime.date.today().year and day.month==datetime.date.today().month and j<=datetime.date.today().day):
                giorni.append(f"{j}❌")
            else:
                giorni.append(f"{j}🟩")
                
    return {
                "giorno": day.day, 
                "mese": month_enToIt[calendar.month_name[day.month]], 
                "anno": day.year, 
                "lista_giorni": giorni 
            }

def build_menu(
    buttons: List[InlineKeyboardButton],
    n_cols: int,
    header_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None,
    footer_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None
) -> List[List[InlineKeyboardButton]]:
    """build_menu()

    Args:
        buttons (List[InlineKeyboardButton]): lista di buttons da visualizzare
        n_cols (int): numero colonne di buttons
        header_buttons (Union[InlineKeyboardButton, List[InlineKeyboardButton]], optional): buttons di testa. Defaults to None.
        footer_buttons (Union[InlineKeyboardButton, List[InlineKeyboardButton]], optional): buttons di coda. Defaults to None.

    Returns:
        List[List[InlineKeyboardButton]]: buttons ordinati come da parametri
    """
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons if isinstance(header_buttons, list) else [header_buttons])
    if footer_buttons:
        menu.append(footer_buttons if isinstance(footer_buttons, list) else [footer_buttons])
    return menu

def insert_whitelist(
    username: str
) -> None:
    """insert_whitelist()

    Args:
        username (str): username da inserire nella whitelist
    """
    with mc.connect(host="localhost",user = "root", passwd="",database="tg_bot",cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(f"INSERT INTO `whitelist` (`username`,`dt_lastLogin`) VALUES ('{username}',CURRENT_TIMESTAMP)")
            __myconn.commit()

def check_whitelist(
    already_logged: bool=False
) -> List[str]:
    """check_whitelist()

    Args:
        already_logged (bool, optional): True controllerà le sessioni degli utenti nella whitelist, 
        False controllerà gli utenti già presenti nella whitelist. Defaults to False.

    Returns:
        List[str]: utenti presenti nella whitelist
    """
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

def update_session(
    username: str
) -> None:
    """update_session()

    Args:
        username (str): utente che deve aggiornare la sessione
    """
    with mc.connect(host="localhost",user = "root", passwd="",database="tg_bot",cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(f"UPDATE `whitelist` SET is_logged=1, dt_lastLogin=CURRENT_TIMESTAMP WHERE username='{username}'")
            __myconn.commit()

def logout(
    username: str
) -> None:
    """logout()

    Args:
        username (str): utente che deve effettuare il logout
    """
    with mc.connect(host="localhost",user = "root", passwd="",database="tg_bot",cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(f"UPDATE `whitelist` SET is_logged=0 WHERE username='{username}'")
            __myconn.commit()

# interfacce

def menu_interface_main(
) -> tuple[str,InlineKeyboardMarkup]:
    keyboard = [
                InlineKeyboardButton("prenotazioni 📅", callback_data='menu_prenotazioni'),
                InlineKeyboardButton("le live demo 🏭", callback_data='menu_liveDemo'),
                InlineKeyboardButton("eventi 🖥️", callback_data='menu_eventi')
        ]
    reply_markup = InlineKeyboardMarkup(build_menu(keyboard,n_cols=1))
    text_reply=f"Schermata principale"
    return text_reply,reply_markup

def menu_interface_menu_prenotazioni(
) -> tuple[str,InlineKeyboardMarkup]:
    keyboard = [
                InlineKeyboardButton("nuova prenotazione", callback_data='new_prenotazione'),
                InlineKeyboardButton("cancella prenotazione", callback_data='delete_prenotazione'),
                InlineKeyboardButton("modifica prenotazioni", callback_data='change_prenotazione'),
                InlineKeyboardButton("le mie prenotazioni", callback_data='my_prenotazione')
        ]
    reply_markup = InlineKeyboardMarkup(build_menu(keyboard,n_cols=1))
    text_reply=f"Interfaccia di prenotazione"
    return text_reply, reply_markup

def calendar_interface(
    firstDayMonth: datetime.date=None,
    busy_days: List[datetime.date]=None,
) -> InlineKeyboardMarkup:
    theDay=dayInfo(firstDayMonth)
    giorno_datetime=firstDayMonth
    mese=theDay["mese"]
    anno=theDay["anno"]
    lista_giorni=theDay["lista_giorni"]

    days=[InlineKeyboardButton(i, callback_data="fashion") for i in ["Lu","Ma","Me","Gi","Ve","Sa","Do"]]
    keyboard=[]
    for i in lista_giorni:
        if i[-1]=="❌" or i==" ":
            keyboard.append(InlineKeyboardButton(i,callback_data="fashion"))
        else:
            keyboard.append(InlineKeyboardButton(i,callback_data=f"{int(i[:-1])}/{giorno_datetime.month}/{giorno_datetime.year}"))

    days+=keyboard
    keyboard=days

    header=[InlineKeyboardButton(f"{mese} {anno}", callback_data="fashion")]
    if giorno_datetime.month==datetime.date.today().month:
        footers=[]
    else:
        footers=[InlineKeyboardButton("indietro",callback_data=f"chMonth_{previous_month(giorno_datetime.month, giorno_datetime.year)}")]

    footers.append(InlineKeyboardButton("avanti",callback_data=f"chMonth_{next_month(giorno_datetime.month, giorno_datetime.year)}"))

    reply_markup=InlineKeyboardMarkup(build_menu(keyboard,n_cols=7, header_buttons= header, footer_buttons=footers))
    return reply_markup

# functions handlers

async def start(
    update: Update,
    context: CallbackContext
) -> None:
    if  "in_conversation" in context.user_data.keys():
        if context.user_data['in_conversation'] == True:
            await update.message.reply_text("Ehi! sei ancora loggato, se vuoi riavviare il bot effettua prima il /logout! o per un semplice riavvio scrivi /cancel !")
            return None
    
    logger.info("Utente \'%s\' ha avviato la conversazione %s.",update.message.from_user.username, update.message.chat_id)
    await update.message.reply_text("Ciao, vi servirò fino alla fine \nDigita il comando /login per utilizzare il bot!\nSe necessario utilizza il comando /cancel per ritornare a questa schermata!")

async def login(
    update: Update, 
    context: CallbackContext
) -> int:
    context.user_data['in_conversation'] = True
    username=update.message.from_user.username
    
    # se è un utente nuovo fa la registrazione
    if username not in check_whitelist():
        logger.info("Utente \'%s\' sta cercando di effettuare il log in.", username)
        await update.message.reply_text(
            "inserisci la password d'accesso: ")
        return LOGIN_CHECK
    # altrimenti rimanda al menù
    else:
        logger.info("Utente \'%s\' è gia registrato. Ha effettuato il log in.", username)
        await context.bot.send_message(chat_id=update.effective_chat.id,text=
            "Sei già loggato nel sistema, accedi al menù con /menu!")
        return MENU

async def login_check(
    update: Update, 
    context: CallbackContext
) -> int:
    
    username=update.message.from_user.username
    passInserita=update.message.text
    messageId=update.message.message_id
    chatId=update.message.chat_id

    # cancellazione messaggi

    await application.bot.delete_message(chat_id=chatId, message_id=messageId)
    # await application.bot.delete_message(chat_id=update.message.chat_id, message_id=messageId-1)
    
    if passInserita=="fromfarmtofork":
        if username not in check_whitelist(True) and username not in check_whitelist():
            insert_whitelist(username)
            logger.info("Log in dell'utente \'%s\' riuscito. Registrazione in corso.", username)  
        else:
            update_session(username)
            logger.info("Log in dell'utente \'%s\' riuscito. Update della sessione.", username)
        await context.bot.send_message(chat_id=chatId,text=
            "Password corretta!\n ora puoi accedere alle funzioni del bot!\nDigita il comando /menu per accedere al menu")
        return MENU
    else:
        logger.info("Log in dell'utente \'%s\' non riuscito. Password usata: %s", username, passInserita)
        # await application.bot.edit_message_text(chat_id=chatId, message_id=update.message.message_id-2, text="riprova a inserire la password:")
        # await update.message.reply_text(
        # "riprova a inserire la password:")
        return LOGIN_CHECK

async def menu(
    update: Update, 
    context: CallbackContext
) -> int:
    username=update.message.from_user.username
    
    # se è un utente nuovo fa la registrazione
    if username not in check_whitelist():
        await context.bot.send_message(chat_id=update.effective_chat.id,text=
            "La sessione è scaduta, ripassa per il /login !")
        context.user_data['in_conversation'] = False
        return ConversationHandler.END
    else:
        update_session(username)
        interfaccia=menu_interface_main()
        await update.message.reply_text(interfaccia[0], reply_markup=interfaccia[1])
        return BUTTON

async def button(
    update: Update, 
    context: CallbackContext
) -> None:
    username=update.callback_query.from_user.username
    
    if username not in check_whitelist():
        await context.bot.send_message(chat_id=update.effective_chat.id,text=
            "La sessione è scaduta, ripassa per il /login !")
        context.user_data['in_conversation'] = False
        return ConversationHandler.END
    else:
        update_session(username)
        query = update.callback_query
        print(f"conferma callback_query: {await query.answer()} query.data:{query.data}")
        
        if query.data=='menu_prenotazioni':
            menu_prenotazioni_interface=menu_interface_menu_prenotazioni()
            await query.edit_message_text(text=menu_prenotazioni_interface[0],reply_markup=menu_prenotazioni_interface[1])
            return BUTTON
        elif query.data=='new_prenotazione' or query.data[:7]=="chMonth":
            # new_prenotazione_interface=menu_interface_new_prenotazione(query.data)
            if query.data[:7]=="chMonth":
                dataSelezionata=query.data.split("_")[-1]
                dayInput=datetime.date(int(dataSelezionata.split("/")[-1]),int(dataSelezionata.split("/")[-2]),int(dataSelezionata.split("/")[-3]))
            else:
                dayInput=datetime.date.today()
            interface_calendar=calendar_interface(dayInput)
            # await query.edit_message_text(text=new_prenotazione_interface[0],reply_markup=new_prenotazione_interface[1])
            await query.edit_message_text(text="seleziona data",reply_markup=interface_calendar)
            return BUTTON
        elif query.data=='fashion':
            await query.answer(text="is_fashion" ,show_alert = True, cache_time=2000)
            return BUTTON
        elif isinstance(datetime.date(int(query.data.split("/")[-1]),int(query.data.split("/")[-2]),int(query.data.split("/")[-3])),datetime.date):
            dataSelezionata=datetime.date(int(query.data.split("/")[-1]),int(query.data.split("/")[-2]),int(query.data.split("/")[-3]))
            await query.edit_message_text(text=f"hai selezionato: {dataSelezionata}")
            return BUTTON
        else: 
            return BUTTON


async def fallback(
    update: Update, 
    context: CallbackContext
) -> int:
    username=update.message.from_user.username
    if update.message.text=="/cancel":
        if username in check_whitelist():
            logger.info("L'utente \'%s\' ha provato a cancellare il login ma risulta loggato.",username)
            await update.message.reply_text(
                "Sei loggato, non puoi effettuare questo comando. In questo caso devi effettuare il comando /logout!")
            return 
        else:
            logger.info("L'utente \'%s\' ha cancellato il log in.",username)
            await update.message.reply_text(
                "Ritorni alla schermata iniziale!")
    else:
        logout(username)
        logger.info("L'utente \'%s\' ha effettuato il logout.",username)
        await update.message.reply_text(
            "Logout effettuato!")

    context.user_data['in_conversation'] = False
    return ConversationHandler.END

def main(

) -> None:
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