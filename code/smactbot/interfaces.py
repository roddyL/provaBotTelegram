# interfaces.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from smactbot.utils import (
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
        InlineKeyboardButton(
            "prenotazioni 📅", callback_data='menu_prenotazioni'),
        InlineKeyboardButton("le live demo 🏭", callback_data='menu_liveDemo'),
        InlineKeyboardButton("eventi 🖥️", callback_data='menu_eventi')
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))
    text_reply = f"Schermata principale"
    return text_reply, reply_markup


def menu_interface_menu_prenotazioni(
) -> tuple[str, InlineKeyboardMarkup]:
    keyboard = [
        InlineKeyboardButton("nuova prenotazione",
                             callback_data='new_prenotazione'),
        InlineKeyboardButton("cancella prenotazione",
                             callback_data='delete_prenotazione'),
        InlineKeyboardButton("modifica prenotazioni",
                             callback_data='change_prenotazione'),
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

def calendar_interface(
    firstDayMonth: datetime.date = None,
    busy_days: List[datetime.date] = None,
) -> InlineKeyboardMarkup:
    theDay = dayInfo(firstDayMonth)
    giorno_datetime = firstDayMonth
    mese = theDay["mese"]
    anno = theDay["anno"]
    lista_giorni = theDay["lista_giorni"]

    days = [InlineKeyboardButton(i, callback_data="fashion") for i in [
        "Lu", "Ma", "Me", "Gi", "Ve", "Sa", "Do"]]
    keyboard = []
    for i in lista_giorni:
        if i[-1] == "❌" or i == " ":
            keyboard.append(InlineKeyboardButton(i, callback_data="fashion"))
        else:
            keyboard.append(InlineKeyboardButton(
                i, callback_data=f"{int(i[:-1])}/{giorno_datetime.month}/{giorno_datetime.year}"))

    days += keyboard
    keyboard = days

    header = [InlineKeyboardButton(f"{mese} {anno}", callback_data="fashion")]
    if giorno_datetime.month == datetime.date.today().month:
        footers = []
    else:
        footers = [InlineKeyboardButton(
            "⬅️", callback_data=f"chMonth_{previous_month(giorno_datetime.month, giorno_datetime.year)}")]

    footers.append(InlineKeyboardButton(
        "➡️", callback_data=f"chMonth_{next_month(giorno_datetime.month, giorno_datetime.year)}"))

    footer_back=[InlineKeyboardButton("⬅️ indietro",
                             callback_data='menu_prenotazioni')]

    reply_markup = InlineKeyboardMarkup(build_menu(
        keyboard, n_cols=7, header_buttons=header, footer_buttons=footers, footer_footer=footer_back))

    text_reply=f"seleziona data"
    return text_reply, reply_markup
