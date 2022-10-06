# !/code/smactbot/utils/utility.py
# Authors:
#     Alberto
#     Loris
"""This module contains all the useful function used across the python project"""

# libraries
from typing import Union, List
import datetime
import calendar
from holidays import italy as italian_holidays
from telegram import InlineKeyboardButton
from smactbot.vars import month_enToIt
import re

# functions

# comments written in italian and not completed

def get_holidays(year: int, province: str) -> List[datetime.date]:
    """giorni_gestivi()

    Args:
        year (int): anno di cui visualizzare i giorni festivi
        provincia (str): codice della provincia che rileva giorni festivi locali  

    Returns:
        List[datetime.date]: lista di giorni festivi
    """
    holidays_list = []
    for the_holidays, _ in sorted(italian_holidays.Italy(subdiv=province, years=year).items()):
        if datetime.date.weekday(the_holidays) != 6:
            holidays_list.append(the_holidays)

    return holidays_list


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
    if mese == 12:
        prossimoMese = f"01/01/{anno+1}"
    else:
        prossimoMese = f"01/{mese+1}/{anno}"

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
    if mese == 1:
        mesePrecedente = f"01/12/{anno-1}"
    else:
        mesePrecedente = f"01/{mese-1}/{anno}"

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
        result += '\x1B[3m' + c
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
    giorni_uffici_pieni: List[datetime.date],
    holidays: List[datetime.date]=[]    
) -> dict:
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

    holidays = list(set(get_holidays(day.year, "PD")) | set(holidays))
    giorni = []
    for i in calendar.monthcalendar(day.year, day.month):
        for j in i:
            if j == 0:
                giorni.append(" ")
            elif datetime.date(day.year, day.month, j) in holidays+giorni_uffici_pieni or i[-1] == j or i[-2] == j or (day.year == datetime.date.today().year and day.month == datetime.date.today().month and j <= datetime.date.today().day):
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
    header_buttons: Union[InlineKeyboardButton,
                          List[InlineKeyboardButton]] = None,
    footer_buttons: Union[InlineKeyboardButton,
                          List[InlineKeyboardButton]] = None,
    footer_footer: Union[InlineKeyboardButton,
                          List[InlineKeyboardButton]] = None
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
        menu.insert(0, header_buttons if isinstance(
            header_buttons, list) else [header_buttons])
    if footer_buttons:
        menu.append(footer_buttons if isinstance(
            footer_buttons, list) else [footer_buttons])
    if footer_footer:
        menu.append(footer_footer if isinstance(
            footer_buttons, list) else [footer_footer])
    return menu

# missing comments all down here

def is_name_or_surname(name_or_surname: str) -> bool:
    pat = "[a-zA-Z ]+"
    sp_char= re.compile("[^[\w ]]")
    if re.match(pat,name_or_surname)and (sp_char.search(name_or_surname) == None):
        return True
    return False

def is_telephone_number(telephone_number: str) -> bool:
    path = "\+?[0-9]{0,2}[-. ]?[0-9]{3}[-. ]?[0-9]{3}[-.]?[0-9]{4}"
    sp_char= re.compile("[^[0-9 +-.]]")
    if re.match(path,telephone_number) and (sp_char.search(telephone_number) == None):
        return True
    return False

def is_mail(mail: str) -> bool:
    pat = "^[a-zA-Z0-9-_.]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pat,mail):
        return True
    return False

def check_contacts(contacts: str) -> bool:
    cont=contacts.split(sep="\n")
    if len(cont)==4:
        if is_name_or_surname(cont[0]) and is_name_or_surname(cont[1]):
            if is_telephone_number(cont[2]):
                if is_mail(cont[3]):
                    return True
    return False

def check_the_contact(contact_type:str, 
                      the_single_contact: str):
    if contact_type=="Name" or contact_type=="Surname":
        return is_name_or_surname(the_single_contact)
    elif contact_type=="TelephoneNumber":
        return is_telephone_number(the_single_contact)
    elif contact_type=="Mail":
        return is_mail(the_single_contact)
    else:
        return False
    

def create_reservation_id(
    reservation_date: datetime.date, 
    n_incremental: int
) -> str:
    return f"{reservation_date}_{n_incremental+1}"
