# interfaces.py

import copy
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from smactbot.models.Gallery import Gallery
from smactbot.models.Prenotazione import Prenotazione
from smactbot.utils.utility import (
    build_menu,
    dayInfo,
    next_month,
    previous_month
)
import datetime
from typing import List
from smactbot.config import *

# interfacce


def menu_interface_main(
    autorizzazioni: dict,
    additionalText: str = ""
) -> tuple[str, InlineKeyboardMarkup]:
    keyboard = []
    authorization_level = autorizzazioni["AuthorizationLevel"]
    if authorization_level <= AUTH_UFFICI:
        keyboard.append(InlineKeyboardButton(
            "uffici 🖥️", callback_data='menu_prenotazioni'))
    if authorization_level <= AUTH_LIVEDEMO:
        keyboard.append(InlineKeyboardButton(
            "le live demo 🏭", callback_data='menu_liveDemo'))
    if authorization_level <= AUTH_EVENTI:
        keyboard.append(InlineKeyboardButton(
            "eventi 📅", callback_data='menu_eventi'))
    if authorization_level <= AUTH_PROFILO:
        keyboard.append(InlineKeyboardButton(
            "il mio profilo 👤", callback_data='menu_profilo'))
    if authorization_level >= AUTH_LOGIN:
        keyboard.append(InlineKeyboardButton("login 👤", callback_data='login'))
    if authorization_level <= AUTH_LOGOUT:
        keyboard.append(InlineKeyboardButton(
            "logout 👤", callback_data='logout'))

    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))
    if additionalText:
        additionalText = f"{additionalText}\n\n"
    text_reply = f"{additionalText}--Schermata principale--\nSei un utente {autorizzazioni['RoleName']} perciò potrai utilizzare solamente queste funzionalità:"
    return text_reply, reply_markup


def menu_profile_interface(
    contatti: str
) -> tuple[str, InlineKeyboardMarkup]:
    keyboard = []
    if contatti:
        text_reply = f"I tuoi contatti:\n{contatti}"
        textModificaOInserisci = "Modifica contatti"
    else:
        text_reply = "Non hai registrato alcun contatto per ora"
        textModificaOInserisci = "Inserisci contatti"

    keyboard.append(InlineKeyboardButton(
        text=textModificaOInserisci, callback_data='menu_modificaContatti'))
    keyboard.append(InlineKeyboardButton("Cancella profilo",
                                         callback_data='menu_cancellaProfilo'))
    keyboard.append(InlineKeyboardButton("↩️ indietro",
                                         callback_data='menu_principale'))

    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))

    return text_reply, reply_markup


def menu_interface_menu_prenotazioni(
    reservation_list: List[dict]
) -> tuple[str, InlineKeyboardMarkup]:

    keyboard = [
        InlineKeyboardButton("nuova prenotazione",
                             callback_data=Prenotazione()),
    ]

    if reservation_list:
        keyboard.append(InlineKeyboardButton("le mie prenotazioni",
                                             callback_data=Gallery(the_class=Prenotazione, the_query=reservation_list)))

    keyboard.append(InlineKeyboardButton("↩️ indietro",
                                         callback_data='menu_principale'))

    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))
    text_reply = f"Interfaccia di prenotazione"
    return text_reply, reply_markup


def menu_interface_menu_liveDemo(
) -> tuple[str, InlineKeyboardMarkup]:
    keyboard = [
        InlineKeyboardButton("le nostre live demo",
                             callback_data='le_liveDemo'),
        InlineKeyboardButton("la live demo più vicina",
                             callback_data='nearest_liveDemo'),
        InlineKeyboardButton("↩️ indietro",
                             callback_data='menu_principale')
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))
    text_reply = f"Interfaccia di prenotazione"
    return text_reply, reply_markup


def interface_nearest_liveDemo(
    maps_url: str,
    text: str
) -> tuple[str, InlineKeyboardMarkup]:
    keyboard = [
        InlineKeyboardButton("Indicazioni 🛣️",
                             url=maps_url),
        InlineKeyboardButton("menu principale 🏠",
                             callback_data='menu_principale')
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))
    text_reply = text
    return text_reply, reply_markup


def back_interface(
    la_callback_data
):
    keyboard = [InlineKeyboardButton(
        "⬅️ indietro", callback_data=la_callback_data)]
    reply_markup = InlineKeyboardMarkup(build_menu(
        keyboard, n_cols=1))
    text_reply = "Premi per ritornare indietro"
    return text_reply, reply_markup


def hours_interface(
    la_prenotazione: Prenotazione,
    busy_hours: List[str]
) -> tuple[str, InlineKeyboardMarkup]:

    fasceOrarie = ["mattino", "pomeriggio", "intera giornata"]
    if len(busy_hours) > 0:
        fasceOrarie.pop()
        if len(busy_hours) > 1:
            fasceOrarie = []
        else:
            fasceOrarie.remove(busy_hours[0])
    keyboard = []
    for i in fasceOrarie:
        copia = copy.deepcopy(la_prenotazione)
        copia.setHours(i)
        keyboard.append(InlineKeyboardButton(i, callback_data=copia))

    if keyboard == []:
        text_reply = f"I posti si sono esauriti per il giorno{la_prenotazione.the_datetime}, mi dispiace!\nTorna indietro e seleziona un'altro giorno"
    else:
        text_reply = f"Seleziona la fascia oraria desiderata per il giorno {la_prenotazione.the_datetime}: "

    copia = copy.deepcopy(la_prenotazione)
    copia.setDatetime(None)
    footers = [InlineKeyboardButton("↩️ indietro",
                                    callback_data=copia)]

    reply_markup = InlineKeyboardMarkup(build_menu(
        keyboard, n_cols=1, footer_buttons=footers))

    return text_reply, reply_markup


def calendar_interface(
    la_prenotazione: Prenotazione,
    giorni_uffici_pieni: List[datetime.date],
    firstDayMonth: datetime.date = None
) -> InlineKeyboardMarkup:
    theDay = dayInfo(day=firstDayMonth,
                     giorni_uffici_pieni=giorni_uffici_pieni)
    giorno_datetime = firstDayMonth
    mese = theDay["mese"]
    anno = theDay["anno"]
    lista_giorni = theDay["lista_giorni"]

    days = [InlineKeyboardButton(i, callback_data=la_prenotazione) for i in [
        "Lu", "Ma", "Me", "Gi", "Ve", "Sa", "Do"]]
    keyboard = []
    for i in lista_giorni:
        if i[-1] == "❌" or i == " ":
            keyboard.append(InlineKeyboardButton(
                i, callback_data=la_prenotazione))
        else:
            copia = copy.deepcopy(la_prenotazione)
            copia.setDatetime(
                the_datetime=datetime.date(
                    day=int(i[:-1]),
                    month=giorno_datetime.month,
                    year=giorno_datetime.year
                )
            )

            keyboard.append(InlineKeyboardButton(
                i, callback_data=copia))

    days += keyboard
    keyboard = days

    header = [InlineKeyboardButton(
        f"{mese} {anno}", callback_data=la_prenotazione)]
    if giorno_datetime.month == datetime.date.today().month:
        header.insert(0, InlineKeyboardButton(
            " ", callback_data=la_prenotazione))
    else:
        the_previous_month = previous_month(
            giorno_datetime.month, giorno_datetime.year)
        copia = copy.deepcopy(la_prenotazione)
        copia.setChMonth(datetime.date(day=int(the_previous_month.split(
            "/")[0]), month=int(the_previous_month.split("/")[1]), year=int(the_previous_month.split("/")[2])))
        header.insert(0, InlineKeyboardButton(
            "⬅️", callback_data=copia))

    the_next_month = next_month(giorno_datetime.month, giorno_datetime.year)
    copia = copy.deepcopy(la_prenotazione)
    copia.setChMonth(datetime.date(day=int(the_next_month.split(
        "/")[0]), month=int(the_next_month.split("/")[1]), year=int(the_next_month.split("/")[2])))
    header.append(InlineKeyboardButton(
        "➡️", callback_data=copia))

    footers = [InlineKeyboardButton("↩️ indietro",
                                    callback_data=Prenotazione())]

    reply_markup = InlineKeyboardMarkup(build_menu(
        keyboard, n_cols=7, header_buttons=header, footer_buttons=footers))

    text_reply = f"seleziona data"
    return text_reply, reply_markup


def confirm_reservation_interface(
    la_prenotazione: Prenotazione
) -> tuple[str, InlineKeyboardMarkup]:
    text_reply = f"Riepilogo prenotazione:\n \
        posti prenotati: {la_prenotazione.seats}\n \
        data: {la_prenotazione.the_datetime}\n \
        fascia oraria: {la_prenotazione.hours}\n\n \
        vuoi confermare la prenotazione?"

    copia = copy.deepcopy(la_prenotazione)
    copia.setHours(None)
    la_prenotazione.setReady(True)
    keyboard = [
        InlineKeyboardButton("conferma",
                             callback_data=la_prenotazione),
        InlineKeyboardButton("↩️ indietro",
                             callback_data=copia)
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))

    return text_reply, reply_markup


def endReservation_interface(
    buonaRiuscita: bool,
    reservation_list: List[dict]
) -> tuple[str, InlineKeyboardMarkup]:
    keyboard = [
        InlineKeyboardButton("Nuova prenotazione",
                             callback_data=Prenotazione())]

    if buonaRiuscita:
        text_reply = f"prenotazione confermata!\nOra scegli se effettuare una nuova prenotazione o ritornare al menu principale!"
        keyboard.append(InlineKeyboardButton("Le mie prenotazioni",
                                             callback_data=Gallery(the_class=Prenotazione, the_query=reservation_list)))
    else:
        text_reply = f"la prenotazione non ha avuto successo\nEffettua per piacere una nuova prenotazione oppure torna al menu principale"

    keyboard.append(InlineKeyboardButton("menu principale 🏠",
                                         callback_data='menu_principale'))

    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))

    return text_reply, reply_markup


def select_ufficio_interface(
    la_prenotazione: Prenotazione,
    lista_uffici: dict,
    autorizzazioni: dict # da aggiungere controllo autorizzazioni per vari uffici
) -> tuple[str, InlineKeyboardMarkup]:
    keyboard = []
    for i in lista_uffici:
        copia = copy.deepcopy(la_prenotazione)
        copia.setUfficio(i["OfficeName"])
        copia.setMaxSeats(i["TotalSeats"])
        keyboard.append(InlineKeyboardButton(i["OfficeName"],
                                             callback_data=copia))
        keyboard.append(InlineKeyboardButton("ℹ️",
                                             callback_data=f"info_{i['Description']}"))

    footer = InlineKeyboardButton("↩️ indietro",
                                  callback_data="menu_prenotazioni")

    reply_markup = InlineKeyboardMarkup(build_menu(
        keyboard, n_cols=2, footer_buttons=footer))
    text_reply = f"Seleziona l'ufficio che ti serve:"

    return text_reply, reply_markup

def seats_interface(
    la_prenotazione: Prenotazione,
    autorizzazioni: dict
) -> tuple[str, InlineKeyboardMarkup]:
    maxPostiUfficio = la_prenotazione.maxSeats
    maxPostiPrenotabili = N_POSTIPRENOTABILI
    if autorizzazioni["AuthorizationLevel"] <= AUTH_MAXPOSTIPRENOTABILI:
        maxPostiPrenotabili = maxPostiUfficio

    keyboard = []
    for posto in range(1, maxPostiPrenotabili+1):
        copia = copy.deepcopy(la_prenotazione)
        copia.setSeatsReady(True)
        copia.setSeats(posto)
        keyboard.append(InlineKeyboardButton(posto,
                                             callback_data=copia))

    for spazioVuoto in range(8 - maxPostiPrenotabili % 8):
        keyboard.append(InlineKeyboardButton(" ",
                                             callback_data=la_prenotazione))

    copia = copy.deepcopy(la_prenotazione)
    copia.setUfficio(None)
    footers = [InlineKeyboardButton("↩️ indietro",
                                    callback_data=copia)]

    reply_markup = InlineKeyboardMarkup(build_menu(keyboard,
                                                   n_cols=8,
                                                   footer_buttons=footers))
    text_reply = f"Seleziona posti da prenotare:"

    return text_reply, reply_markup


def myPrenotazioni_interface(
    la_galleria: Gallery
) -> tuple[str, InlineKeyboardMarkup]:

    strBack = "⬅️"
    strNext = "➡️"
    copiaBack = copy.deepcopy(la_galleria)
    copiaNext = copy.deepcopy(la_galleria)
    copiaDelete = copy.deepcopy(la_galleria)
    copiaDelete.isDeletingChange()

    if la_galleria.pos == 0:
        strBack = " "
    if la_galleria.pos == la_galleria.size-1:
        strNext = " "

    copiaBack.back()
    copiaNext.next()

    keyboard = [
        InlineKeyboardButton(strBack,
                             callback_data=copiaBack),
        InlineKeyboardButton(strNext,
                             callback_data=copiaNext),
        # InlineKeyboardButton("modifica",
        #                      callback_data="fashion"),
        InlineKeyboardButton("cancella",
                             callback_data=copiaDelete)
    ]

    footers = [InlineKeyboardButton("↩️ indietro",
                                    callback_data="menu_prenotazioni")]
    text_reply = la_galleria.show()
    reply_markup = InlineKeyboardMarkup(build_menu(keyboard,
                                                   n_cols=2,
                                                   footer_buttons=footers))

    return text_reply, reply_markup


def delete_prenotazioni_interface(
    la_galleria: Gallery
) -> tuple[str, InlineKeyboardMarkup]:

    copiaAnnulla = copy.deepcopy(la_galleria)
    copiaConferma = copy.deepcopy(la_galleria)
    copiaAnnulla.isDeletingChange()
    copiaConferma.isReadyDeleteChange()

    keyboard = [
        InlineKeyboardButton("annulla",
                             callback_data=copiaAnnulla),
        InlineKeyboardButton("conferma",
                             callback_data=copiaConferma)
    ]

    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=2))

    text_reply = f"{la_galleria.show()}\nSei sicuro di cancellare questa prenotazione?"
    return text_reply, reply_markup


def deleteConfirm_prenotazioni_interface(
    la_galleria: Gallery
) -> tuple[str, InlineKeyboardMarkup]:

    keyboard = []

    if la_galleria.delete():
        text_reply = "Prenotazione cancellata con successo!\nOra scegli se tornare alle tue prenotazioni o al menu"
    else:
        text_reply = "Purtroppo non siamo riusciti a cancellare la tua prenotazione, contatta la segreteria per ottenere ulteriore supporto"

    if la_galleria.size > 0:
        keyboard.append(InlineKeyboardButton("le mie prenotazioni",
                                             callback_data=la_galleria))

    keyboard.append(InlineKeyboardButton("menu principale",
                                         callback_data="menu_principale"))

    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))

    return text_reply, reply_markup


def cancellaProfilo_interface():
    text_reply = "Sei sicuro di cancellare tutti i dati che detiene il bot, ovvero i dati di sistema, i contatti e le prenotazioni?"
    keyboard = [
        InlineKeyboardButton("annulla",
                             callback_data="menu_profilo"),
        InlineKeyboardButton("conferma",
                             callback_data="cancella_dati")
    ]

    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=2))

    return text_reply, reply_markup


def menu_changeProfile_interface():
    text_reply = "Puoi modificare e/o inserire i seguenti campi:"
    keyboard = [
        InlineKeyboardButton("nome",
                             callback_data="menu_modificaNome"),
        InlineKeyboardButton("cognome",
                             callback_data="menu_modificaCognome"),
        InlineKeyboardButton("numero",
                             callback_data="menu_modificaNumero"),
        InlineKeyboardButton("mail",
                             callback_data="menu_modificaMail"),
        InlineKeyboardButton("↩️ indietro",
                             callback_data="menu_profilo")
    ]

    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))

    return text_reply, reply_markup
