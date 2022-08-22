# handlers.py

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from smactbot.vars import (
    BUTTON,
    LOGIN,
    LOGIN_CHECK,
    MENU
)
import datetime
from smactbot.log import logger
from smactbot.db_functions import (
    insert_whitelist,
    check_whitelist,
    update_session,
    logout
)

from smactbot.interfaces import (
    menu_interface_main,
    menu_interface_menu_prenotazioni,
    calendar_interface
)

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
    if update.message.text == "/cancel":
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
    else:
        logout(username)
        logger.info("L'utente \'%s\' ha effettuato il logout.", username)
        await update.message.reply_text(
            "Logout effettuato!")

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
            insert_whitelist(username)
            logger.info(
                "Log in dell'utente \'%s\' riuscito. Registrazione in corso.", username)
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
        interfaccia = menu_interface_main()
        await update.message.reply_text(interfaccia[0], reply_markup=interfaccia[1])
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

        if query.data == 'menu_prenotazioni':
            menu_prenotazioni_interface = menu_interface_menu_prenotazioni()
            await query.edit_message_text(text=menu_prenotazioni_interface[0], reply_markup=menu_prenotazioni_interface[1])
            return BUTTON
        elif query.data == 'new_prenotazione' or query.data[:7] == "chMonth":
            # new_prenotazione_interface=menu_interface_new_prenotazione(query.data)
            if query.data[:7] == "chMonth":
                dataSelezionata = query.data.split("_")[-1]
                dayInput = datetime.date(int(dataSelezionata.split(
                    "/")[-1]), int(dataSelezionata.split("/")[-2]), int(dataSelezionata.split("/")[-3]))
            else:
                dayInput = datetime.date.today()
            interface_calendar = calendar_interface(dayInput)
            # await query.edit_message_text(text=new_prenotazione_interface[0],reply_markup=new_prenotazione_interface[1])
            await query.edit_message_text(text=interface_calendar[0], reply_markup=interface_calendar[1])
            return BUTTON
        elif query.data == 'fashion':
            await query.answer(text="is_fashion", show_alert=True, cache_time=2000)
            return BUTTON
        elif isinstance(datetime.date(int(query.data.split("/")[-1]), int(query.data.split("/")[-2]), int(query.data.split("/")[-3])), datetime.date):
            dataSelezionata = datetime.date(int(query.data.split(
                "/")[-1]), int(query.data.split("/")[-2]), int(query.data.split("/")[-3]))
            await query.edit_message_text(text=f"hai selezionato: {dataSelezionata}")
            return BUTTON
        else:
            return BUTTON
