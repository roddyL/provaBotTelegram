# interfaces.py

from cProfile import label
from cgitb import text
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
        InlineKeyboardButton("↩️ indietro",
                             callback_data='menu_principale')
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))
    text_reply = f"I tuoi contatti:\n{contatti}"
    return text_reply, reply_markup

def menu_interface_menu_prenotazioni(
    risultato_query: List[dict]
) -> tuple[str, InlineKeyboardMarkup]:

    keyboard = [
        InlineKeyboardButton("nuova prenotazione",
                             callback_data=Prenotazione()),
    ]

    if risultato_query:
        keyboard.append(InlineKeyboardButton("le mie prenotazioni",
                         callback_data=Gallery(the_class=Prenotazione,the_query=risultato_query)))

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
    keyboard=[InlineKeyboardButton("⬅️ indietro",callback_data=la_callback_data)]
    reply_markup=InlineKeyboardMarkup(build_menu(
        keyboard, n_cols=1))
    text_reply="Premi per ritornare indietro"
    return text_reply, reply_markup

def hours_interface(
    la_prenotazione: Prenotazione,
    busy_hours: List[str]
) -> tuple[str, InlineKeyboardMarkup]:

    fasceOrarie=["mattino", "pomeriggio", "intera giornata"]
    if len(busy_hours)>0:
        fasceOrarie.pop()
        if len(busy_hours)>1:
            fasceOrarie=[]
        else:
            fasceOrarie.remove(busy_hours[0])
    keyboard = []
    for i in fasceOrarie:
        copia=copy.deepcopy(la_prenotazione)
        copia.setHours(i)
        keyboard.append(InlineKeyboardButton(i,callback_data=copia))

    if keyboard == []:
        text_reply = f"I posti si sono esauriti per il giorno{la_prenotazione.the_datetime}, mi dispiace!\nTorna indietro e seleziona un'altro giorno"
    else:
        text_reply = f"Seleziona la fascia oraria desiderata per il giorno {la_prenotazione.the_datetime}: "

    copia=copy.deepcopy(la_prenotazione)
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
    theDay = dayInfo(day=firstDayMonth, giorni_uffici_pieni=giorni_uffici_pieni)
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

    footer_back = [InlineKeyboardButton("↩️ indietro",
                                        callback_data=Prenotazione())]

    reply_markup = InlineKeyboardMarkup(build_menu(
        keyboard, n_cols=7, header_buttons=header, footer_buttons=footers, footer_footer=footer_back))

    text_reply = f"seleziona data"
    return text_reply, reply_markup

def confirm_reservation_interface(
    telegram_id: int,
    la_prenotazione: Prenotazione
) -> tuple[str, InlineKeyboardMarkup]:
    text_reply=f"Riepilogo prenotazione:\n \
        posti prenotati: {la_prenotazione.seats}\n \
        data: {la_prenotazione.the_datetime}\n \
        fascia oraria: {la_prenotazione.hours}\n\n \
        vuoi confermare la prenotazione?"
    
    copia=copy.deepcopy(la_prenotazione)
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
    risultato_query: List[dict]
) -> tuple[str, InlineKeyboardMarkup]:
    keyboard = [
        InlineKeyboardButton("Nuova prenotazione",
                            callback_data=Prenotazione())]

    if buonaRiuscita:
        text_reply = f"prenotazione confermata!\nOra scegli se effettuare una nuova prenotazione o ritornare al menu principale!"
        keyboard.append(InlineKeyboardButton("Le mie prenotazioni",
                            callback_data=Gallery(the_class=Prenotazione,the_query=risultato_query)))
    else:
        text_reply = f"la prenotazione non ha avuto successo\nEffettua per piacere una nuova prenotazione oppure torna al menu principale"

    keyboard.append(InlineKeyboardButton("menu principale 🏠",
                            callback_data='menu_principale'))

    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))

    return text_reply, reply_markup

def seats_interface(
    la_prenotazione: Prenotazione
) -> tuple[str, InlineKeyboardMarkup]:
    maxPostiPrenotabili=15
    
    
    
    copiaMin=copy.deepcopy(la_prenotazione)
    copiaAdd=copy.deepcopy(la_prenotazione)
    if la_prenotazione.seats>=maxPostiPrenotabili:
        copiaMin.setSeats(la_prenotazione.seats-1)
        strMax=" "
        strMin="➖"
    elif la_prenotazione.seats<=1:
        copiaAdd.setSeats(la_prenotazione.seats+1)
        strMax="➕"
        strMin=" "
    else:
        copiaMin.setSeats(la_prenotazione.seats-1) 
        copiaAdd.setSeats(la_prenotazione.seats+1)
        strMax="➕"
        strMin="➖"

    la_prenotazione.setSeatsReady(True)

    keyboard=[
            InlineKeyboardButton(strMin, 
                                 callback_data=copiaMin),
            InlineKeyboardButton("conferma", 
                                 callback_data=la_prenotazione),
            InlineKeyboardButton(strMax, 
                                 callback_data=copiaAdd),
    ]

    footers = [InlineKeyboardButton("↩️ indietro",
                                    callback_data="menu_prenotazioni")]
    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=3, footer_buttons=footers))
    text_reply=f"Seleziona posti da prenotare.\nPosti: {la_prenotazione.seats}"

    return text_reply, reply_markup

def myPrenotazioni_interface(
    la_galleria: Gallery
) -> tuple[str, InlineKeyboardMarkup]:
    
    strBack="⬅️"
    strNext="➡️"
    copiaBack=copy.deepcopy(la_galleria)
    copiaNext=copy.deepcopy(la_galleria)
    copiaDelete=copy.deepcopy(la_galleria)
    copiaDelete.isDeletingChange()
    
    if la_galleria.pos==0:
        strBack=" "
    if la_galleria.pos==la_galleria.size-1:
        strNext=" "

    copiaBack.back()
    copiaNext.next()


    keyboard=[
            InlineKeyboardButton(strBack, 
                                 callback_data=copiaBack),
            InlineKeyboardButton(strNext, 
                                 callback_data=copiaNext),
            InlineKeyboardButton("modifica",
                                 callback_data="fashion"),
            InlineKeyboardButton("cancella",
                                 callback_data=copiaDelete)
    ]

    footers = [InlineKeyboardButton("↩️ indietro",
                                    callback_data="menu_prenotazioni")]
    text_reply=la_galleria.show()
    reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=2, footer_buttons=footers))

    return text_reply, reply_markup

def delete_prenotazioni_interface(
    la_galleria: Gallery
) -> tuple[str, InlineKeyboardMarkup]:
    
    copiaAnnulla=copy.deepcopy(la_galleria)
    copiaConferma=copy.deepcopy(la_galleria)
    copiaAnnulla.isDeletingChange()
    copiaConferma.isReadyDeleteChange()

    keyboard=[
            InlineKeyboardButton("annulla", 
                                 callback_data=copiaAnnulla),
            InlineKeyboardButton("conferma", 
                                 callback_data=copiaConferma)
    ]

    reply_markup=InlineKeyboardMarkup(build_menu(keyboard, n_cols=2))

    text_reply=f"{la_galleria.show()}\nSei sicuro di cancellare questa prenotazione?"
    return text_reply, reply_markup

def deleteConfirm_prenotazioni_interface(
    la_galleria: Gallery
) -> tuple[str, InlineKeyboardMarkup]:
    
    keyboard=[]

    if la_galleria.delete():
        text_reply="Prenotazione cancellata con successo!\nOra scegli se tornare alle tue prenotazioni o al menu"
    else:
        text_reply="Purtroppo non siamo riusciti a cancellare la tua prenotazione, contatta la segreteria per ottenere ulteriore supporto"
    
    if la_galleria.size>0:
        keyboard.append(InlineKeyboardButton("le mie prenotazioni", 
                                    callback_data=la_galleria))

    keyboard.append(InlineKeyboardButton("menu principale", 
                                callback_data="menu_principale"))
    

    reply_markup=InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))

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
