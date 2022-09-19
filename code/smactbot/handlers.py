# handlers.py

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from smactbot.models import Prenotazione

from smactbot.vars import *
from smactbot.utils.liveDemo_geolocation import nearest_production

from smactbot.log import logger
from smactbot.db_functions import *

from smactbot.interfaces import *
from smactbot.decorators import session_check

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
    username = update.message.from_user.username
    telegram_id=update.message.from_user.id
    
    # if "in_conversation" in context.user_data.keys():
    #     if context.user_data['in_conversation'] == True:
    #         await update.message.reply_text("Ehi! sei ancora loggato, se vuoi riavviare il bot effettua prima il /logout! o per un semplice riavvio scrivi /cancel !")
    #         return

    logger.info("Utente \'%s\' con id \'%s\' ha avviato la conversazione %s.",
                update.message.from_user.username, update.message.from_user.id, update.message.chat_id)
    if username:
        insert_firstStart(telegram_id=telegram_id, username=username)
    else:
        insert_firstStart(telegram_id=telegram_id)
        
    additionalText="Ciao, vi servirò fino alla fine \nPremi il tasto login per utilizzare il bot con tutte le sue funzionalità!"
    menu_main_interface = menu_interface_main(autorizzazioni=return_auth(telegram_id=telegram_id), additionalText=additionalText)
    await update.message.reply_text(menu_main_interface[0], reply_markup=menu_main_interface[1])
    return BUTTON


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
    telegram_id=update.message.from_user.id
    chatId=update.message.chat_id
    comando=update.message.text
    # if comando == "/cancel":
    #     if telegram_id in check_whitelist():
    #         logger.info(
    #             "L'utente \'%s\' con id \'%s\' ha provato a cancellare il login ma risulta loggato.", username, telegram_id)
    #         await update.message.reply_text(
    #             "Sei loggato, non puoi effettuare questo comando. In questo caso devi effettuare il comando /logout!")
    #         return
    #     else:
    #         logger.info("L'utente \'%s\' con id \'%s\' ha cancellato il log in.", username, telegram_id)
    #         await update.message.reply_text(
    #             "Ritorni alla schermata iniziale!")
    # elif comando=="/logout" and telegram_id in check_whitelist():
    #     logout(telegram_id=telegram_id)
    #     change_role(telegram_id=telegram_id, nome_ruolo="guest")
        
    #     # inserire store di tutta la chat
        
    #     logger.info("L'utente \'%s\' con id \'%s\' ha effettuato il logout.", username, telegram_id)
    #     await update.message.reply_text(
    #         "Logout effettuato!")
    if comando=="/back":
        logger.info(
            f"L'utente {username} con id {telegram_id} ha digitato il comando /back")
        il_back=context.user_data["back"]
        if isinstance(il_back, int):
            return il_back
        else:
            interfaccia_back=back_interface(il_back)
            await context.bot.send_message(chat_id=chatId, text=interfaccia_back[0], reply_markup=interfaccia_back[1])
            return BUTTON
    # else:
    #     return LOGIN_CHECK

    # context.user_data['in_conversation'] = False
    # return ConversationHandler.END


# async def login(
#     update: Update,
#     context: CallbackContext
# ) -> int:
#     """login()

#     Args:
#         update (Update): update del bot
#         context (CallbackContext): contesto del bot

#     Returns:
#         int: prossima schermata
#     """
#     context.user_data['in_conversation'] = True
#     username = update.message.from_user.username
#     telegram_id = update.message.from_user.id
#     # se è un utente nuovo fa la registrazione
#     if telegram_id not in check_whitelist():
#         logger.info(
#             "Utente \'%s\' con id \'%s\' sta cercando di effettuare il log in.", username, telegram_id)
#         await update.message.reply_text(
#             "inserisci la password d'accesso: ")
#         return LOGIN_CHECK
    # altrimenti rimanda al menù
    # else:
    #     logger.info(
    #         "Utente \'%s\' con id \'%s\' è gia registrato. Ha effettuato il log in.", username, telegram_id)
    #     await context.bot.send_message(chat_id=update.effective_chat.id, text="Sei già loggato nel sistema, accedi al menù con /menu!")
    #     return MENU


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
    telegram_id = update.message.from_user.id
    chatId = update.message.chat_id

    # cancellazione messaggi
    context.user_data["to_delete"].append(update.message.id)
    for i in context.user_data["to_delete"]:
        await context.bot.delete_message(chat_id=chatId, message_id=i)
    
    context.user_data["to_delete"]=[]

    if passInserita == "fromfarmtofork":
        if not check_whitelist(telegram_id=telegram_id):
            # context.user_data["logged"]=True
            logger.info(
                "Log in dell'utente \'%s\' con id \'%s\' riuscito. Registrazione in corso.", username, telegram_id)
            # fai partire la richiesta dei contatti
            await context.bot.send_message(chat_id=chatId, 
                                            text="Password corretta!\n Ora inserisci i tuoi contatti in questo modo:\nNome\nCognome\nnumero di telefono\nla tua mail")
            change_role(telegram_id=telegram_id, nome_ruolo="admin")
            return CONTACTS
        else:
            update_session(telegram_id=telegram_id)
            change_role(telegram_id=telegram_id, nome_ruolo="admin")
            logger.info(
                "Log in dell'utente \'%s\' con id \'%s\' riuscito. Update della sessione.", username, telegram_id)
        messaggio=await context.bot.send_message(chat_id=chatId, 
                                        text="Password corretta!\n ora puoi accedere alle funzioni del bot!")
        context.user_data["to_delete"].append(messaggio.id)
        menu_main_interface = menu_interface_main(autorizzazioni=return_auth(telegram_id=telegram_id))
        await update.message.reply_text(menu_main_interface[0], reply_markup=menu_main_interface[1])
        return BUTTON
        # return MENU
    else:
        logger.info(
            "Log in dell'utente \'%s\' con id \'%s\' non riuscito. Password usata: %s", username, telegram_id, passInserita)
        return LOGIN_CHECK

# @session_check
# async def menu(
#     update: Update,
#     context: CallbackContext
# ) -> int:
#     """menu()

#     Args:
#         update (Update): update del bot
#         context (CallbackContext): contesto del bot

#     Returns:
#         int: prossima schermata
#     """
#     telegram_id = update.message.from_user.id
#     menu_main_interface = menu_interface_main(autorizzazioni=return_auth(telegram_id=telegram_id))
#     await update.message.reply_text(menu_main_interface[0], reply_markup=menu_main_interface[1])
#     return BUTTON

@session_check
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
    telegram_id = update.callback_query.from_user.id
    query = update.callback_query
    chat_id=query.message.chat_id
    logger.info(f"conferma callback_query dell'utente {username} con id {telegram_id}: query.data:{query.data}")

    if isinstance(query.data,Prenotazione):
        this_prenotazione=query.data

        if not this_prenotazione.seatsReady:
            interfaccia = seats_interface(la_prenotazione=this_prenotazione, autorizzazioni=return_auth(telegram_id=telegram_id))
        elif this_prenotazione.chMonth:
            this_prenotazione.setMonthSelected(this_prenotazione.chMonth) 
            this_prenotazione.setChMonth(None)
            interfaccia = calendar_interface(firstDayMonth=this_prenotazione.monthSelected, 
                                                la_prenotazione=this_prenotazione, 
                                                giorni_uffici_pieni=check_busyDays(posti_daPrenotare=this_prenotazione.seats, 
                                                                                monthSelected=this_prenotazione.monthSelected))
        elif not this_prenotazione.the_datetime:
            interfaccia = calendar_interface(firstDayMonth=this_prenotazione.monthSelected, 
                                                la_prenotazione=this_prenotazione, 
                                                giorni_uffici_pieni=check_busyDays(posti_daPrenotare=this_prenotazione.seats, 
                                                                                    monthSelected=this_prenotazione.monthSelected))
        elif not this_prenotazione.hours:
            interfaccia = hours_interface(la_prenotazione=this_prenotazione, 
                                            busy_hours=check_busyHours(data=this_prenotazione.the_datetime, 
                                            posti_daPrenotare=this_prenotazione.seats))
        elif not this_prenotazione.ready:
            if not this_prenotazione.isUpdating:
                interfaccia= confirm_reservation_interface(la_prenotazione=this_prenotazione)
            else:
                pass
        else:
            interfaccia=endReservation_interface(this_prenotazione.conferma(telegram_id=telegram_id),
                                                    risultato_query=show_prenotazioni(telegram_id=telegram_id))
    
    elif isinstance(query.data, Gallery):
        this_gallery=query.data

        if this_gallery.size>0:
            if not this_gallery.isDeleting:
                interfaccia=myPrenotazioni_interface(this_gallery)
            else:
                if not this_gallery.isReadyDelete:
                    interfaccia=delete_prenotazioni_interface(this_gallery)
                else:
                    interfaccia=deleteConfirm_prenotazioni_interface(this_gallery)
        else:
            return BUTTON
    elif isinstance(query.data, str): 
        if query.data=="login":
            # context.user_data['in_conversation'] = True
            context.user_data['back']="menu_principale"
            logger.info(
                "Utente \'%s\' con id \'%s\' sta cercando di effettuare il log in.", username, telegram_id)
            messaggio=await context.bot.send_message(
                chat_id=chat_id,
                text="inserisci la password d'accesso: \n\
                    digita /back per tornare alla schermata precedente"
                )
            context.user_data["to_delete"]=[messaggio.id]
            return LOGIN_CHECK
        elif query.data == "menu_principale":
            interfaccia = menu_interface_main(autorizzazioni=return_auth(telegram_id=telegram_id))
        elif query.data == 'menu_liveDemo':
            interfaccia = menu_interface_menu_liveDemo()
        elif query.data == 'nearest_liveDemo':
            context.user_data['back']="menu_liveDemo"
            await query.edit_message_text("mandami la tua posizione e ti saprò dire la live demo più vicina a te! \ndigita il comando /back per tornare alla schermata precedente")
            return LOCATION
        elif query.data == 'menu_prenotazioni':
            interfaccia = menu_interface_menu_prenotazioni(risultato_query=show_prenotazioni(telegram_id=telegram_id))
        elif query.data == "menu_profilo":
            interfaccia=menu_profile_interface(show_contacts(telegram_id=telegram_id))
        elif query.data == 'menu_cancellaProfilo':
            interfaccia=cancellaProfilo_interface()
        elif query.data == 'cancella_dati':
            delete_data(telegram_id=telegram_id)
            await query.edit_message_text(text="Hai cancellato tutti i tuoi dati. \nSe vuoi ricominciare una nuova conversazione con il bot digita /start")
            return ConversationHandler.END
        elif query.data == "logout":
            # logout(telegram_id=telegram_id)
            change_role(telegram_id=telegram_id, 
                        nome_ruolo="guest")
            
            # inserire store di tutta la chat
            
            logger.info("L'utente \'%s\' con id \'%s\' ha effettuato il logout.", username, telegram_id)
            # await context.bot.send_message(chat_id=chat_id,
            #                                text="Ciao, hai effettuato il logout! \nPremi il tasto login per utilizzare il bot con tutte le sue funzionalità!")
            additionalText="Ciao, hai effettuato il logout!"
            interfaccia = menu_interface_main(autorizzazioni=return_auth(telegram_id=telegram_id),additionalText=additionalText)            
        else:
            await query.answer(text="Questa funzione non è stata ancora implementata", show_alert=True)
            return BUTTON
        
    await query.edit_message_text(text=interfaccia[0], 
                                  reply_markup=interfaccia[1])
    return BUTTON

@session_check
async def send_location(
    update: Update,
    context: CallbackContext
) -> int:
    username = update.message.from_user.username
    telegram_id = update.message.from_user.id
    posizione = update.message.location
    chatId = update.message.chat_id
    
    await update.message.delete()
    logger.info(
        f"Posizione dell'utente {username} con id {telegram_id}: longitudine: {posizione.latitude} latitudine:{posizione.longitude}")

    sedeVicina=nearest_production(posizione)
    
    location_interface = interface_nearest_liveDemo(
        maps_url=sedeVicina[1], text=sedeVicina[0])
    await context.bot.send_message(chat_id=chatId, 
                                   text=location_interface[0], 
                                   reply_markup=location_interface[1])

    return BUTTON

async def send_contacts(
    update: Update,
    context: CallbackContext
) -> int:
    
    username = update.message.from_user.username
    telegram_id = update.message.from_user.id
    contatti = update.message.text
    chatId = update.message.chat_id

    # if not context.user_data['logged']==True:
    #     await context.bot.send_message(chat_id=update.effective_chat.id, 
    #                                    text="La sessione è scaduta, ripassa per il /login !")

    await update.message.delete()
    logger.info(
        f"I contatti dell'utente {username} con id {telegram_id}: {contatti}")

    if insert_contacts(telegram_id=telegram_id, 
                       username=username, 
                       contatti=contatti):
        await context.bot.send_message(chat_id=chatId, 
                                       text="Hai registrato i tuoi contatti!\nOra puoi accedere alle funzioni del bot!")
        menu_main_interface = menu_interface_main(autorizzazioni=return_auth(telegram_id=telegram_id))
        await update.message.reply_text(menu_main_interface[0], 
                                        reply_markup=menu_main_interface[1])
        return BUTTON
    else:
        await context.bot.send_message(chat_id=chatId, 
                                       text="Attenzione, hai sbagliato ad inserire i contatti correttamente.\nTi invitiamo a rispettare le regole perfettamente")
        return CONTACTS
    