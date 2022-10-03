# handlers.py

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from smactbot.utils.utility import isNameSurname, isMail, isPhoneNumber
from smactbot.models import Prenotazione, ShowInformation

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

    username = update.message.from_user.username
    telegram_id = update.message.from_user.id
    context.user_data["to_delete"] = list()
    logger.info("Utente \'%s\' con id \'%s\' ha avviato la conversazione %s.",
                update.message.from_user.username, update.message.from_user.id, update.message.chat_id)

    insert_first_start(telegram_id=telegram_id, username=username)

    additionalText = "Ciao, vi servirò fino alla fine \nPremi il tasto login per utilizzare il bot con tutte le sue funzionalità!"
    menu_main_interface = menu_interface_main(autorizzazioni=check_authorization(
        telegram_id=telegram_id), additionalText=additionalText)
    await update.message.reply_text(menu_main_interface[0], reply_markup=menu_main_interface[1])
    return BUTTON


async def fallback(
    update: Update,
    context: CallbackContext
) -> int:

    username = update.message.from_user.username
    telegram_id = update.message.from_user.id
    chat_id = update.message.chat_id
    comando = update.message.text

    if comando == "/back":
        logger.info(
            f"L'utente {username} con id {telegram_id} ha digitato il comando /back")

        context.user_data["to_delete"].append(update.message.id)

        while len(context.user_data["to_delete"]) > 0:
            await context.bot.delete_message(chat_id=chat_id, message_id=context.user_data["to_delete"].pop())

        il_back = context.user_data["back"]
        if isinstance(il_back, int):
            return il_back
        else:
            interfaccia_back = back_interface(il_back)
            await context.bot.send_message(chat_id=chat_id, text=interfaccia_back[0], reply_markup=interfaccia_back[1])
            return BUTTON


async def login_check(
    update: Update,
    context: CallbackContext
) -> int:

    username = update.message.from_user.username
    typed_password = update.message.text
    telegram_id = update.message.from_user.id
    chat_id = update.message.chat_id

    # cancellazione messaggi
    context.user_data["to_delete"].append(update.message.id)

    while len(context.user_data["to_delete"]) > 0:
        await context.bot.delete_message(chat_id=chat_id, message_id=context.user_data["to_delete"].pop())

    context.user_data["to_delete"] = []

    role_passwords = get_role_password()
    if typed_password in role_passwords.keys():
        if not check_whitelist(telegram_id=telegram_id):
            logger.info(
                "Log in dell'utente \'%s\' con id \'%s\' riuscito. Registrazione in corso.", username, telegram_id)
            # fai partire la richiesta dei contatti
            await context.bot.send_message(chat_id=chat_id,
                                           text="Password corretta!\n Ora inserisci il tuo nome:")
            change_role(telegram_id=telegram_id,
                        role_name=role_passwords[typed_password])
            context.user_data['back'] = "login"
            insert_whitelist(telegram_id=telegram_id)
            return CONTACT_NAME
        else:
            update_session(telegram_id=telegram_id)
            change_role(telegram_id=telegram_id,
                        role_name=role_passwords[typed_password])
            logger.info(
                "Log in dell'utente \'%s\' con id \'%s\' riuscito. Update della sessione.", username, telegram_id)
        messaggio = await context.bot.send_message(chat_id=chat_id,
                                                   text="Password corretta!\n ora puoi accedere alle funzioni del bot!")
        context.user_data["to_delete"].append(messaggio.id)
        menu_main_interface = menu_interface_main(
            autorizzazioni=check_authorization(telegram_id=telegram_id))
        await update.message.reply_text(menu_main_interface[0], reply_markup=menu_main_interface[1])
        return BUTTON
    else:
        logger.info(
            "Log in dell'utente \'%s\' con id \'%s\' non riuscito. Password usata: %s", username, telegram_id, typed_password)
        messaggio = await context.bot.send_message(chat_id=chat_id,
                                                   text="Password SBAGLIATA!\n Riprova a inserire la password.\nPremi /back per tornare indietro")
        context.user_data["to_delete"].append(messaggio.id)
        return LOGIN_CHECK


@session_check
async def button(
    update: Update,
    context: CallbackContext
) -> int:

    username = update.callback_query.from_user.username
    telegram_id = update.callback_query.from_user.id
    query = update.callback_query
    chat_id = query.message.chat_id
    logger.info(
        f"conferma callback_query dell'utente {username} con id {telegram_id}: query.data:{query.data}")

    while len(context.user_data["to_delete"]) > 0:
        await context.bot.delete_message(chat_id=chat_id, 
                                         message_id=context.user_data["to_delete"].pop())

    if isinstance(query.data, Prenotazione):
        this_prenotazione = query.data

        if not this_prenotazione.nome_ufficio:
            interfaccia = select_ufficio_interface(la_prenotazione=this_prenotazione, lista_uffici=get_office(
            ), autorizzazioni=check_authorization(telegram_id=telegram_id))
        elif not this_prenotazione.seatsReady:
            interfaccia = seats_interface(
                la_prenotazione=this_prenotazione, autorizzazioni=check_authorization(telegram_id=telegram_id))
        elif this_prenotazione.chMonth:
            this_prenotazione.setMonthSelected(this_prenotazione.chMonth)
            this_prenotazione.setChMonth(None)
            interfaccia = calendar_interface(firstDayMonth=this_prenotazione.monthSelected,
                                             la_prenotazione=this_prenotazione,
                                             giorni_uffici_pieni=check_busy_days(reserved_seats=this_prenotazione.seats,
                                                                                 selected_month=this_prenotazione.monthSelected,
                                                                                 office_name=this_prenotazione.nome_ufficio))
        elif not this_prenotazione.the_datetime:
            interfaccia = calendar_interface(firstDayMonth=this_prenotazione.monthSelected,
                                             la_prenotazione=this_prenotazione,
                                             giorni_uffici_pieni=check_busy_days(reserved_seats=this_prenotazione.seats,
                                                                                 selected_month=this_prenotazione.monthSelected,
                                                                                 office_name=this_prenotazione.nome_ufficio))
        elif not this_prenotazione.hours:
            interfaccia = hours_interface(la_prenotazione=this_prenotazione,
                                          busy_hours=check_busy_time_period(reservation_date=this_prenotazione.the_datetime,
                                                                            reserved_seats=this_prenotazione.seats,
                                                                            office_name=this_prenotazione.nome_ufficio))
        elif not this_prenotazione.ready:
            if not this_prenotazione.isUpdating:
                interfaccia = confirm_reservation_interface(
                    la_prenotazione=this_prenotazione)
            else:
                pass
        else:
            interfaccia = endReservation_interface(this_prenotazione.conferma(telegram_id=telegram_id),
                                                   reservation_list=show_reservations(telegram_id=telegram_id))

    elif isinstance(query.data, Gallery):
        this_gallery = query.data
        if this_gallery.the_class == Prenotazione and this_gallery.size > 0:
            if not this_gallery.isDeleting:
                interfaccia = myPrenotazioni_interface(this_gallery)
            else:
                if not this_gallery.isReadyDelete:
                    interfaccia = delete_prenotazioni_interface(this_gallery)
                else:
                    interfaccia = deleteConfirm_prenotazioni_interface(
                        this_gallery)
        elif this_gallery.the_class == ShowInformation:
            pass
        else:
            return BUTTON

    elif isinstance(query.data, str):
        if query.data == "login":
            context.user_data['back'] = "menu_principale"
            logger.info(
                "Utente \'%s\' con id \'%s\' sta cercando di effettuare il log in.", username, telegram_id)
            messaggio = await query.edit_message_text(
                text="inserisci la password d'accesso: \n\
                    digita /back per tornare alla schermata precedente"
            )
            context.user_data["to_delete"] = [messaggio.id]
            return LOGIN_CHECK
        elif query.data == "menu_principale":
            interfaccia = menu_interface_main(
                autorizzazioni=check_authorization(telegram_id=telegram_id))
        elif query.data == 'menu_liveDemo':
            interfaccia = menu_interface_menu_liveDemo()
        elif query.data == 'nearest_liveDemo':
            context.user_data['back'] = "menu_liveDemo"
            messaggio = await query.edit_message_text("mandami la tua posizione e ti saprò dire la live demo più vicina a te! \ndigita il comando /back per tornare alla schermata precedente")
            context.user_data["to_delete"] = [messaggio.id]
            return LOCATION
        elif query.data == 'menu_prenotazioni':
            interfaccia = menu_interface_menu_prenotazioni(
                reservation_list=show_reservations(telegram_id=telegram_id))
        elif query.data == "menu_profilo":
            interfaccia = menu_profile_interface(
                show_contacts(telegram_id=telegram_id))
        elif query.data == "menu_modificaContatti":
            interfaccia = menu_changeProfile_interface()
        elif query.data == "menu_modificaNome":
            context.user_data['back'] = "menu_profilo"
            # logger.info(
            #     "Utente \'%s\' con id \'%s\' sta cercando di effettuare il log in.", username, telegram_id)
            messaggio = await query.edit_message_text(
                text="inserisci il tuo nome: \n\
                    digita /back per tornare alla schermata precedente"
            )
            context.user_data["to_delete"] = [messaggio.id]
            return CONTACT_NAME
        elif query.data == "menu_modificaCognome":
            context.user_data['back'] = "menu_profilo"
            # logger.info(
            #     "Utente \'%s\' con id \'%s\' sta cercando di effettuare il log in.", username, telegram_id)
            messaggio = await query.edit_message_text(
                text="inserisci il tuo cognome: \n\
                    digita /back per tornare alla schermata precedente"
            )
            context.user_data["to_delete"] = [messaggio.id]
            return CONTACT_SURNAME
        elif query.data == "menu_modificaNumero":
            context.user_data['back'] = "menu_profilo"
            # logger.info(
            #     "Utente \'%s\' con id \'%s\' sta cercando di effettuare il log in.", username, telegram_id)
            messaggio = await query.edit_message_text(
                text="inserisci il tuo numero di telefono: \n\
                    digita /back per tornare alla schermata precedente"
            )
            context.user_data["to_delete"] = [messaggio.id]
            return CONTACT_NUMBER
        elif query.data == "menu_modificaMail":
            context.user_data['back'] = "menu_profilo"
            # logger.info(
            #     "Utente \'%s\' con id \'%s\' sta cercando di effettuare il log in.", username, telegram_id)
            messaggio = await query.edit_message_text(
                text="inserisci la tua mail: \n\
                    digita /back per tornare alla schermata precedente"
            )
            context.user_data["to_delete"] = [messaggio.id]
            return CONTACT_MAIL
        elif query.data == 'menu_cancellaProfilo':
            interfaccia = cancellaProfilo_interface()
        elif query.data == 'cancella_dati':
            delete_data(telegram_id=telegram_id)
            await query.edit_message_text(text="Hai cancellato tutti i tuoi dati. \nSe vuoi ricominciare una nuova conversazione con il bot digita /start")
            return ConversationHandler.END
        elif query.data == "logout":
            # logout(telegram_id=telegram_id)
            change_role(telegram_id=telegram_id,
                        role_name="guest")

            # inserire store di tutta la chat

            logger.info(
                "L'utente \'%s\' con id \'%s\' ha effettuato il logout.", username, telegram_id)
            additionalText = "Ciao, hai effettuato il logout!"
            interfaccia = menu_interface_main(autorizzazioni=check_authorization(
                telegram_id=telegram_id), additionalText=additionalText)
        else:
            if query.data.split("_")[0] == "info":
                text = query.data.split("_")[1]
            else:
                text = "Questa funzione non è stata ancora implementata"
            await query.answer(text=text, show_alert=True)
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
    chat_id = update.message.chat_id

    context.user_data["to_delete"].append(update.message.id)
    while len(context.user_data["to_delete"]) > 0:
        await context.bot.delete_message(chat_id=chat_id, message_id=context.user_data["to_delete"].pop())

    logger.info(
        f"Posizione dell'utente {username} con id {telegram_id}: longitudine: {posizione.latitude} latitudine:{posizione.longitude}")

    nearest_branch = nearest_production(posizione)

    location_interface = interface_nearest_liveDemo(
        maps_url=nearest_branch[1], text=nearest_branch[0])
    await context.bot.send_message(chat_id=chat_id,
                                   text=location_interface[0],
                                   reply_markup=location_interface[1])

    return BUTTON


async def send_contact_name(
    update: Update,
    context: CallbackContext
) -> int:

    return await send_contact_generic(
        update=update,
        context=context,
        contact_type="Name",
        msg_currentAction="il tuo nome",
        msg_nextAction="all'inserimento del tuo cognome",
        current_return=CONTACT_NAME,
        next_return=CONTACT_SURNAME
    )


async def send_contact_surname(
    update: Update,
    context: CallbackContext
) -> int:

    return await send_contact_generic(
        update=update,
        context=context,
        contact_type="Surname",
        msg_currentAction="il tuo cognome",
        msg_nextAction="all'inserimento del tuo numero di telefono",
        current_return=CONTACT_SURNAME,
        next_return=CONTACT_NUMBER
    )


async def send_contact_number(
    update: Update,
    context: CallbackContext
) -> int:

    return await send_contact_generic(
        update=update,
        context=context,
        contact_type="TelephoneNumber",
        msg_currentAction="il tuo numero di telefono",
        msg_nextAction="all'inserimento della tua mail",
        current_return=CONTACT_NUMBER,
        next_return=CONTACT_MAIL
    )


async def send_contact_mail(
    update: Update,
    context: CallbackContext
) -> int:

    return await send_contact_generic(
        update=update,
        context=context,
        contact_type="Mail",
        msg_currentAction="la tua mail",
        msg_nextAction="al menu principale",
        current_return=CONTACT_MAIL,
        next_return=BUTTON
    )


async def send_contact_generic(
    update: Update,
    context: CallbackContext,
    contact_type: str,
    msg_currentAction: str,
    msg_nextAction: str,
    current_return: int,
    next_return: int
) -> int:

    telegram_id = update.message.from_user.id
    chat_id = update.message.chat_id
    message_id = update.message.id
    message = update.message.text

    while len(context.user_data["to_delete"]) > 0:
        await context.bot.delete_message(chat_id=chat_id, message_id=context.user_data["to_delete"].pop())

    if insert_contacts(telegram_id=telegram_id, contact_type=contact_type, the_single_contact=message):
        if context.user_data['back'] != "menu_profilo":
            # schermata subito dopo il login

            il_messaggio = await context.bot.send_message(chat_id=chat_id,
                                                          text=f"Hai registrato correttamente {msg_currentAction}, ora passa {msg_nextAction}:")
            if next_return == BUTTON:
                interfaccia = menu_interface_main(
                    autorizzazioni=check_authorization(telegram_id=telegram_id))
                await context.bot.send_message(chat_id=chat_id,
                                               text=interfaccia[0],
                                               reply_markup=interfaccia[1])
            the_return = next_return
        else:
            il_messaggio = await context.bot.send_message(chat_id=chat_id,
                                                          text=f"Hai registrato correttamente {msg_currentAction}!")
            interfaccia = menu_changeProfile_interface()
            await context.bot.send_message(chat_id=chat_id, text=interfaccia[0],
                                           reply_markup=interfaccia[1])
            the_return = BUTTON
    else:
        il_messaggio = await context.bot.send_message(chat_id=chat_id,
                                                      text=f"Non hai inserito correttamente {msg_currentAction}, riprova")

        the_return = current_return

    context.user_data["to_delete"].append(il_messaggio.id)
    context.user_data["to_delete"].append(message_id)
    return the_return
