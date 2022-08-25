# interfaces.py

import copy
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from smactbot.models.Prenotazione import Prenotazione
from smactbot.utils.utility import (
    build_menu,
    dayInfo,
    next_month,
    previous_month
)
import datetime
from typing import List

# interfacce

def menu_interface_main(
) -> tuple[str, InlineKeyboardMarkup]:
    keyboard = [
        InlineKeyboardButton("prenotazioni 📅", callback_data='menu_prenotazioni'),
        InlineKeyboardButton("le live demo 🏭", callback_data='menu_liveDemo'),
        InlineKeyboardButton("eventi 🖥️", callback_data='menu_eventi'),
        InlineKeyboardButton("il mio profilo 👤", callback_data='menu_profilo'),
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))
    text_reply = f"Schermata principale"
    return text_reply, reply_markup

def menu_profile_interface(
    contatti: str
) -> tuple[str, InlineKeyboardMarkup]:
    keyboard = [
        InlineKeyboardButton("Modifica contatti", callback_data='menu_modificaContatti'),
        InlineKeyboardButton("Cancella profilo", callback_data='menu_cancellaProfilo'),
        InlineKeyboardButton("⬅️ indietro",
                             callback_data='menu_principale')
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))
    text_reply = f"I tuoi contatti:\n{contatti}"
    return text_reply, reply_markup

def menu_interface_menu_prenotazioni(
) -> tuple[str, InlineKeyboardMarkup]:
    keyboard = [
        # InlineKeyboardButton("nuova prenotazione",
        #                      callback_data='new_prenotazione'),
        InlineKeyboardButton("nuova prenotazione",
                             callback_data=Prenotazione()),
        InlineKeyboardButton("le mie prenotazioni",
                             callback_data='my_prenotazione'),
        InlineKeyboardButton("⬅️ indietro",
                             callback_data='menu_principale')
    ]
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
        InlineKeyboardButton("⬅️ indietro",
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
    keyboard=[InlineKeyboardButton("⬅️ indietro",callback_data=la_callback_data)]
    reply_markup=InlineKeyboardMarkup(build_menu(
        keyboard, n_cols=1))
    text_reply="Premi per ritornare indietro"
    return text_reply, reply_markup

def hours_interface(
    la_prenotazione: Prenotazione,
    fasceOrarie: List[str] = ["mattino", "pomeriggio"],
) -> tuple[str, InlineKeyboardMarkup]:

    keyboard = []
    for i in fasceOrarie:
        copia=copy.deepcopy(la_prenotazione)
        copia.setHours(i)
        keyboard.append(InlineKeyboardButton(i,
                                             callback_data=copia)
                        )

    if keyboard == []:
        text_reply = f"I posti si sono esauriti per il giorno{la_prenotazione.the_datetime}, mi dispiace!\nTorna indietro e seleziona un'altro giorno"
    else:
        text_reply = f"Seleziona la fascia oraria desiderata per il giorno {la_prenotazione.the_datetime}: "

    copia=copy.deepcopy(la_prenotazione)
    copia.setDatetime(None)
    footers = [InlineKeyboardButton("⬅️ indietro",
                                    callback_data=copia)]

    reply_markup = InlineKeyboardMarkup(build_menu(
        keyboard, n_cols=1, footer_buttons=footers))

    return text_reply, reply_markup

def calendar_interface(
    la_prenotazione: Prenotazione,
    firstDayMonth: datetime.date = None,
    busy_days: List[datetime.date] = None,
) -> InlineKeyboardMarkup:
    theDay = dayInfo(firstDayMonth)
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
            copia=copy.deepcopy(la_prenotazione)
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
        footers = []
    else:
        the_previous_month = previous_month(
            giorno_datetime.month, giorno_datetime.year)
        copia=copy.deepcopy(la_prenotazione)
        copia.setChMonth(datetime.date(day=int(the_previous_month.split(
            "/")[0]), month=int(the_previous_month.split("/")[1]), year=int(the_previous_month.split("/")[2])))
        footers = [InlineKeyboardButton(
            "⬅️", callback_data=copia)]

    the_next_month = next_month(giorno_datetime.month, giorno_datetime.year)
    copia=copy.deepcopy(la_prenotazione)
    copia.setChMonth(datetime.date(day=int(the_next_month.split(
        "/")[0]), month=int(the_next_month.split("/")[1]), year=int(the_next_month.split("/")[2])))
    footers.append(InlineKeyboardButton(
        "➡️", callback_data=copia))

    footer_back = [InlineKeyboardButton("⬅️ indietro",
                                        callback_data=Prenotazione())]

    reply_markup = InlineKeyboardMarkup(build_menu(
        keyboard, n_cols=7, header_buttons=header, footer_buttons=footers, footer_footer=footer_back))

    text_reply = f"seleziona data"
    return text_reply, reply_markup

# def calendar_interface(
#     firstDayMonth: datetime.date = None,
#     busy_days: List[datetime.date] = None,
# ) -> InlineKeyboardMarkup:
#     theDay = dayInfo(firstDayMonth)
#     giorno_datetime = firstDayMonth
#     mese = theDay["mese"]
#     anno = theDay["anno"]
#     lista_giorni = theDay["lista_giorni"]

#     days = [InlineKeyboardButton(i, callback_data="fashion") for i in [
#         "Lu", "Ma", "Me", "Gi", "Ve", "Sa", "Do"]]
#     keyboard = []
#     for i in lista_giorni:
#         if i[-1] == "❌" or i == " ":
#             keyboard.append(InlineKeyboardButton(i, callback_data="fashion"))
#         else:
#             keyboard.append(InlineKeyboardButton(
#                 i, callback_data=f"{int(i[:-1])}/{giorno_datetime.month}/{giorno_datetime.year}"))

#     days += keyboard
#     keyboard = days

#     header = [InlineKeyboardButton(f"{mese} {anno}", callback_data="fashion")]
#     if giorno_datetime.month == datetime.date.today().month:
#         footers = []
#     else:
#         footers = [InlineKeyboardButton(
#             "⬅️", callback_data=f"chMonth_{previous_month(giorno_datetime.month, giorno_datetime.year)}")]

#     footers.append(InlineKeyboardButton(
#         "➡️", callback_data=f"chMonth_{next_month(giorno_datetime.month, giorno_datetime.year)}"))

#     footer_back = [InlineKeyboardButton("⬅️ indietro",
#                                         callback_data='menu_prenotazioni')]

#     reply_markup = InlineKeyboardMarkup(build_menu(
#         keyboard, n_cols=7, header_buttons=header, footer_buttons=footers, footer_footer=footer_back))

#     text_reply = f"seleziona data"
#     return text_reply, reply_markup
# 
# # def hours_interface(
#     giornoSelezionato: str,
#     fasceOrarie: List[str] = ["mattino", "pomeriggio"]
# ) -> tuple[str, InlineKeyboardMarkup]:

#     keyboard = []
#     for i in fasceOrarie:
#         keyboard.append(InlineKeyboardButton(i, callback_data=f'fascia_{i}'))

#     if keyboard == []:
#         text_reply = f"I posti si sono esauriti per il giorno{giornoSelezionato}, mi dispiace!\nTorna indietro e seleziona un'altro giorno"
#     else:
#         text_reply = f"Seleziona la fascia oraria desiderata per il giorno {giornoSelezionato}: "

#     footers = [InlineKeyboardButton("⬅️ indietro",
#                                     callback_data='new_prenotazione')]

#     reply_markup = InlineKeyboardMarkup(build_menu(
#         keyboard, n_cols=1, footer_buttons=footers))

#     return text_reply, reply_markup
