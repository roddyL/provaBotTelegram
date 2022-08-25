# handlers.py

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from smactbot.models import Prenotazione

from smactbot.vars import *
from smactbot.utils.liveDemo_geolocation import nearest_production

import datetime
from smactbot.log import logger
from smactbot.db_functions import *

from smactbot.interfaces import *

# functions handlers


async def start(
    update: Update,
    context: CallbackContext
) -> None:
    """start()

    Args:
        update (Update): update del bot
        context (CallbackContext): contesto del bot

    Returns:
        _type_: None
    """
    if "in_conversation" in context.user_data.keys():
        if context.user_data['in_conversation'] == True:
            await update.message.reply_text("Ehi! sei ancora loggato, se vuoi riavviare il bot effettua prima il /logout! o per un semplice riavvio scrivi /cancel !")
            return None

    logger.info("Utente \'%s\' ha avviato la conversazione %s.",
                update.message.from_user.username, update.message.chat_id)
    await update.message.reply_text("Ciao, vi servirò fino alla fine \nDigita il comando /login per utilizzare il bot!\nSe necessario utilizza il comando /cancel per ritornare a questa schermata!")


async def fallback(
    update: Update,
    context: CallbackContext
) -> int:
    """fallback()

    Args:
        update (Update): update del bot
        context (CallbackContext): contesto del bot

    Returns:
        int: prossima schermata
    """
    username = update.message.from_user.username
    chatId=update.message.chat_id
    comando=update.message.text
    if comando == "/cancel":
        if username in check_whitelist():
            logger.info(
                "L'utente \'%s\' ha provato a cancellare il login ma risulta loggato.", username)
            await update.message.reply_text(
                "Sei loggato, non puoi effettuare questo comando. In questo caso devi effettuare il comando /logout!")
            return
        else:
            logger.info("L'utente \'%s\' ha cancellato il log in.", username)
            await update.message.reply_text(
                "Ritorni alla schermata iniziale!")
    elif comando=="/logout" and username in check_whitelist():
        logout(username)
        logger.info("L'utente \'%s\' ha effettuato il logout.", username)
        await update.message.reply_text(
            "Logout effettuato!")
    elif comando=="/back" and username in check_whitelist():
        logger.info(
            f"L'utente {username} ha digitato il comando /back")
        il_back=context.user_data["back"]
        if isinstance(il_back, int):
            return il_back
        else:
            interfaccia_back=back_interface(il_back)
            await context.bot.send_message(chat_id=chatId, text=interfaccia_back[0], reply_markup=interfaccia_back[1])
            return BUTTON
    else:
        return LOGIN_CHECK

    context.user_data['in_conversation'] = False
    return ConversationHandler.END


async def login(
    update: Update,
    context: CallbackContext
) -> int:
    """login()

    Args:
        update (Update): update del bot
        context (CallbackContext): contesto del bot

    Returns:
        int: prossima schermata
    """
    context.user_data['in_conversation'] = True
    username = update.message.from_user.username

    # se è un utente nuovo fa la registrazione
    if username not in check_whitelist():
        logger.info(
            "Utente \'%s\' sta cercando di effettuare il log in.", username)
        await update.message.reply_text(
            "inserisci la password d'accesso: ")
        return LOGIN_CHECK
    # altrimenti rimanda al menù
    else:
        logger.info(
            "Utente \'%s\' è gia registrato. Ha effettuato il log in.", username)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sei già loggato nel sistema, accedi al menù con /menu!")
        return MENU


async def login_check(
    update: Update,
    context: CallbackContext
) -> int:
    """login_check()

    Args:
        update (Update): update del bot
        context (CallbackContext): contesto del bot

    Returns:
        int: prossima schermata
    """
    username = update.message.from_user.username
    passInserita = update.message.text
    # messageId = update.message.message_id
    chatId = update.message.chat_id

    # cancellazione messaggi
    await update.message.delete()

    if passInserita == "fromfarmtofork":
        if username not in check_whitelist(True) and username not in check_whitelist():
            context.user_data["logged"]=True
            logger.info(
                "Log in dell'utente \'%s\' riuscito. Registrazione in corso.", username)
            # fai partire la richiesta dei contatti
            await context.bot.send_message(chat_id=chatId, text="Password corretta!\n Ora inserisci i tuoi contatti in questo modo:\nNome\nCognome\nnumero di telefono\nla tua mail")
            return CONTACTS
        else:
            update_session(username)
            logger.info(
                "Log in dell'utente \'%s\' riuscito. Update della sessione.", username)
        await context.bot.send_message(chat_id=chatId, text="Password corretta!\n ora puoi accedere alle funzioni del bot!\nDigita il comando /menu per accedere al menu")
        return MENU
    else:
        logger.info(
            "Log in dell'utente \'%s\' non riuscito. Password usata: %s", username, passInserita)
        return LOGIN_CHECK


async def menu(
    update: Update,
    context: CallbackContext
) -> int:
    """menu()

    Args:
        update (Update): update del bot
        context (CallbackContext): contesto del bot

    Returns:
        int: prossima schermata
    """
    username = update.message.from_user.username

    # se è un utente nuovo fa la registrazione
    if username not in check_whitelist():
        await context.bot.send_message(chat_id=update.effective_chat.id, text="La sessione è scaduta, ripassa per il /login !")
        context.user_data['in_conversation'] = False
        return ConversationHandler.END
    else:
        update_session(username)
        menu_main_interface = menu_interface_main()
        await update.message.reply_text(menu_main_interface[0], reply_markup=menu_main_interface[1])
        return BUTTON


async def button(
    update: Update,
    context: CallbackContext
) -> int:
    """button()

    Args:
        update (Update): update del bot
        context (CallbackContext): contesto del bot

    Returns:
        int: prossima schermata
    """
    username = update.callback_query.from_user.username

    if username not in check_whitelist():
        await context.bot.send_message(chat_id=update.effective_chat.id, text="La sessione è scaduta, ripassa per il /login !")
        context.user_data['in_conversation'] = False
        return ConversationHandler.END
    else:
        update_session(username)
        query = update.callback_query
        logger.info(f"conferma callback_query dell'utente {username}: {await query.answer()} query.data:{query.data}")

        if isinstance(query.data,Prenotazione):
            print("c'è un oggetto prenotazione")
            this_prenotazione=query.data
            context.user_data['this_prenotazione']=this_prenotazione
            if not this_prenotazione.seats:
                context.user_data['back']="menu_prenotazioni"
                await query.edit_message_text("Inserisci il numero di posti da prenotare: \ndigita il comando /back per tornare alla schermata precedente")
                return SEATS
            elif this_prenotazione.chMonth:
                dayInput = this_prenotazione.chMonth
                this_prenotazione.setChMonth(None)
                interface_calendar = calendar_interface(firstDayMonth=dayInput, la_prenotazione=this_prenotazione)
                await query.edit_message_text(text=interface_calendar[0], reply_markup=interface_calendar[1])
                return BUTTON
            elif not this_prenotazione.the_datetime:
                context.user_data['back']=SEATS
                interface_calendar = calendar_interface(firstDayMonth=datetime.date.today(), la_prenotazione=this_prenotazione)
                await query.edit_message_text(text=interface_calendar[0], reply_markup=interface_calendar[1])
                return BUTTON
            elif not this_prenotazione.hours:
                interfaccia_hours = hours_interface(la_prenotazione=this_prenotazione)
                await query.edit_message_text(text=interfaccia_hours[0], reply_markup=interfaccia_hours[1])
                return BUTTON
            else:
                # dai conferma della prenotazione o torni indietro
                pass
        elif isinstance(query.data, str): 
            if query.data == "menu_principale":
                menu_main_interface = menu_interface_main()
                await query.edit_message_text(menu_main_interface[0], reply_markup=menu_main_interface[1])
                return BUTTON
            elif query.data == 'menu_liveDemo':
                menu_liveDemo_interface = menu_interface_menu_liveDemo()
                await query.edit_message_text(menu_liveDemo_interface[0], reply_markup=menu_liveDemo_interface[1])
                return BUTTON
            elif query.data == 'nearest_liveDemo':
                context.user_data['back']="menu_liveDemo"
                await query.edit_message_text("mandami la tua posizione e ti saprò dire la live demo più vicina a te! \ndigita il comando /back per tornare alla schermata precedente")
                return LOCATION
            elif query.data == 'menu_prenotazioni':
                menu_prenotazioni_interface = menu_interface_menu_prenotazioni()
                await query.edit_message_text(text=menu_prenotazioni_interface[0], reply_markup=menu_prenotazioni_interface[1])
                return BUTTON
            elif query.data == "menu_profilo":
                interfaccia_profilo=menu_profile_interface(show_contacts(username=username))
                await query.edit_message_text(text=interfaccia_profilo[0], reply_markup=interfaccia_profilo[1])
                return BUTTON
            # elif query.data == 'new_prenotazione' or query.data[:7] == "chMonth":
            #     # new_prenotazione_interface=menu_interface_new_prenotazione(query.data)
            #     if query.data[:7] == "chMonth":
            #         dataSelezionata = query.data.split("_")[-1]
            #         dayInput = datetime.date(int(dataSelezionata.split(
            #             "/")[-1]), int(dataSelezionata.split("/")[-2]), int(dataSelezionata.split("/")[-3]))
            #     else:
            #         dayInput = datetime.date.today()
            #     interface_calendar = calendar_interface(dayInput)
            #     # await query.edit_message_text(text=new_prenotazione_interface[0],reply_markup=new_prenotazione_interface[1])
            #     await query.edit_message_text(text=interface_calendar[0], reply_markup=interface_calendar[1])
            #     return BUTTON
            # elif query.data == 'fashion':
            #     await query.answer(text="is_fashion", show_alert=True, cache_time=2000)
            #     return BUTTON
            # elif isinstance(datetime.date(int(query.data.split("/")[-1]), int(query.data.split("/")[-2]), int(query.data.split("/")[-3])), datetime.date):
            #     dataSelezionata = datetime.date(int(query.data.split(
            #         "/")[-1]), int(query.data.split("/")[-2]), int(query.data.split("/")[-3]))
            #     interfaccia_fasceOrarie=hours_interface(dataSelezionata)
            #     await query.edit_message_text(text=interfaccia_fasceOrarie[0],reply_markup=interfaccia_fasceOrarie[1])
            #     return BUTTON
            else:
                return BUTTON


async def send_location(
    update: Update,
    context: CallbackContext
) -> int:
    username = update.message.from_user.username
    posizione = update.message.location
    chatId = update.message.chat_id

    if username not in check_whitelist():
        await context.bot.send_message(chat_id=update.effective_chat.id, text="La sessione è scaduta, ripassa per il /login !")
        context.user_data['in_conversation'] = False
        return ConversationHandler.END
    else:
        update_session(username)

    await update.message.delete()
    logger.info(
        f"Posizione dell'utente {username}: longitudine: {posizione.latitude} latitudine:{posizione.longitude}")

    sedeVicina=nearest_production(posizione)
    
    location_interface = interface_nearest_liveDemo(
        maps_url=sedeVicina[1], text=sedeVicina[0])
    await context.bot.send_message(chat_id=chatId, text=location_interface[0], reply_markup=location_interface[1])

    return BUTTON

async def send_seats(
    update: Update,
    context: CallbackContext
) -> int:
    
    username = update.message.from_user.username
    seats = update.message.text
    chatId = update.message.chat_id

    if username not in check_whitelist():
        await context.bot.send_message(chat_id=update.effective_chat.id, text="La sessione è scaduta, ripassa per il /login !")
        context.user_data['in_conversation'] = False
        return ConversationHandler.END
    else:
        update_session(username)

    await update.message.delete()
    logger.info(
        f"Posti selezionati dall'utente {username}: {seats}")
    this_prenotazione=context.user_data['this_prenotazione']
    # this_prenotazione=Prenotazione()
    this_prenotazione.setSeats(int(seats))
    interfaccia_calendar=calendar_interface(firstDayMonth=datetime.date.today(), la_prenotazione=this_prenotazione)
    await context.bot.send_message(chat_id=chatId, text=interfaccia_calendar[0], reply_markup=interfaccia_calendar[1])
    return BUTTON

async def send_contacts(
    update: Update,
    context: CallbackContext
) -> int:
    
    username = update.message.from_user.username
    contatti = update.message.text
    chatId = update.message.chat_id

    if not context.user_data['logged']==True:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="La sessione è scaduta, ripassa per il /login !")

    await update.message.delete()
    logger.info(
        f"I contatti dell'utente {username}: {contatti}")

    if insert_contacts(username, contatti):
        await context.bot.send_message(chat_id=chatId, text="Hai registrato i tuoi contatti!\nOra puoi accedere alle funzioni del bot!\nDigita il comando /menu per accedere al menu")
        return MENU
    else:
        await context.bot.send_message(chat_id=chatId, text="Attenzione, hai sbagliato ad inserire i contatti correttamente.\nTi invitiamo a rispettare le regole perfettamente")
        return CONTACTS
    