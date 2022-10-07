# !/code/smactbot/TgButtonInterface.py
# Authors:
#     Alberto
#     Loris
"""This module contains all the interfaces for the buttons menu"""

# libraries
import copy
import datetime
from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from smactbot.models.Gallery import Gallery
from smactbot.models.Reservation import Reservation
from smactbot.utils.utility import (
    build_menu,
    day_info,
    next_month,
    previous_month
)
from smactbot.config import *

# interfaces
class TgButtonInterface():

    @classmethod
    def main_menu(
        cls,
        role_authorization: dict,
        additional_text: str = ""
    ) -> tuple[str, InlineKeyboardMarkup]:
        keyboard = []
        authorization_level = role_authorization["AuthorizationLevel"]
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
        if additional_text:
            additional_text = f"{additional_text}\n\n"
        text_reply = f"{additional_text}--Schermata principale--\nSei un utente {role_authorization['RoleName']} perciò potrai utilizzare solamente queste funzionalità:"
        return text_reply, reply_markup

    @classmethod
    def profile_menu(
        cls,
        contacts: str
    ) -> tuple[str, InlineKeyboardMarkup]:
        keyboard = []
        if contacts:
            text_reply = f"I tuoi contatti:\n{contacts}"
            type_of_action_text = "Modifica contatti"
        else:
            text_reply = "Non hai registrato alcun contatto per ora"
            type_of_action_text = "Inserisci contatti"

        keyboard.append(InlineKeyboardButton(
            text=type_of_action_text, callback_data='menu_modificaContatti'))
        keyboard.append(InlineKeyboardButton("Cancella profilo",
                                            callback_data='menu_cancellaProfilo'))
        keyboard.append(InlineKeyboardButton("↩️ indietro",
                                            callback_data='menu_principale'))

        reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))

        return text_reply, reply_markup

    @classmethod
    def reservations_menu(
        cls,
        reservations_list: List[dict]
    ) -> tuple[str, InlineKeyboardMarkup]:

        keyboard = [
            InlineKeyboardButton("nuova prenotazione",
                                callback_data=Reservation()),
        ]

        if reservations_list:
            keyboard.append(InlineKeyboardButton("le mie prenotazioni",
                                                callback_data=Gallery(the_class=Reservation, the_query=reservations_list)))

        keyboard.append(InlineKeyboardButton("↩️ indietro",
                                            callback_data='menu_principale'))

        reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))
        text_reply = f"Interfaccia di prenotazione"
        return text_reply, reply_markup

    @classmethod
    def livedemo_menu(
        cls
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
        text_reply = f"Interfaccia di visualizzazione live demo"
        return text_reply, reply_markup

    @classmethod
    def end_nearest_livedemo_action(
        cls,
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

    @classmethod
    def back_action(
        cls,
        la_callback_data
    ):
        keyboard = [InlineKeyboardButton(
            "⬅️ indietro", callback_data=la_callback_data)]
        reply_markup = InlineKeyboardMarkup(build_menu(
            keyboard, n_cols=1))
        text_reply = "Premi per ritornare indietro"
        return text_reply, reply_markup

    @classmethod
    def time_period_selection(
        cls,
        the_reservation: Reservation,
        busy_time_periods: List[str]
    ) -> tuple[str, InlineKeyboardMarkup]:

        the_time_periods = ["mattino", "pomeriggio", "intera giornata"]
        if len(busy_time_periods) > 0:
            the_time_periods.pop()
            if len(busy_time_periods) > 1:
                the_time_periods = []
            else:
                the_time_periods.remove(busy_time_periods[0])
        keyboard = []
        for i in the_time_periods:
            object_copy = copy.deepcopy(the_reservation)
            object_copy.time_period = i
            keyboard.append(InlineKeyboardButton(i, callback_data=object_copy))

        if keyboard == []:
            text_reply = f"I posti si sono esauriti per il giorno{the_reservation.reservation_date}, mi dispiace!\nTorna indietro e seleziona un'altro giorno"
        else:
            text_reply = f"Seleziona la fascia oraria desiderata per il giorno {the_reservation.reservation_date}: "

        object_copy = copy.deepcopy(the_reservation)
        object_copy.reservation_date = None
        footers = [InlineKeyboardButton("↩️ indietro",
                                        callback_data=object_copy)]

        reply_markup = InlineKeyboardMarkup(build_menu(
            keyboard, n_cols=1, footer_buttons=footers))

        return text_reply, reply_markup

    @classmethod
    def reservation_date_selection(
        cls,
        the_reservation: Reservation,
        full_office_days: List[datetime.date],
        first_day_of_the_month: datetime.date = None
    ) -> InlineKeyboardMarkup:
        the_day = day_info(day=first_day_of_the_month,
                        full_office_days=full_office_days)
        first_day_of_showed_month = first_day_of_the_month
        month = the_day["month"]
        year = the_day["year"]
        days_list = the_day["days_list"]

        days = [InlineKeyboardButton(i, callback_data=the_reservation) for i in [
            "Lu", "Ma", "Me", "Gi", "Ve", "Sa", "Do"]]
        keyboard = []
        for a_day in days_list:
            if a_day[-1] == "❌" or a_day == " ":
                keyboard.append(InlineKeyboardButton(
                    a_day, callback_data=the_reservation))
            else:
                object_copy = copy.deepcopy(the_reservation)
                object_copy.reservation_date = datetime.date(
                        day=int(a_day[:-1]),
                        month=first_day_of_showed_month.month,
                        year=first_day_of_showed_month.year
                    )

                keyboard.append(InlineKeyboardButton(
                    a_day, callback_data=object_copy))

        days += keyboard
        keyboard = days

        header = [InlineKeyboardButton(
            f"{month} {year}", callback_data=the_reservation)]
        if first_day_of_showed_month.month == datetime.date.today().month:
            header.insert(0, InlineKeyboardButton(
                " ", callback_data=the_reservation))
        else:
            the_previous_month = previous_month(
                first_day_of_showed_month.month, first_day_of_showed_month.year)
            object_copy = copy.deepcopy(the_reservation)
            object_copy.next_month_to_show = datetime.date(day=int(the_previous_month.split(
                "/")[0]), month=int(the_previous_month.split("/")[1]), year=int(the_previous_month.split("/")[2]))
            header.insert(0, InlineKeyboardButton(
                "⬅️", callback_data=object_copy))

        the_next_month = next_month(first_day_of_showed_month.month, first_day_of_showed_month.year)
        object_copy = copy.deepcopy(the_reservation)
        object_copy.next_month_to_show = datetime.date(day=int(the_next_month.split(
            "/")[0]), month=int(the_next_month.split("/")[1]), year=int(the_next_month.split("/")[2]))
        header.append(InlineKeyboardButton(
            "➡️", callback_data=object_copy))

        footers = [InlineKeyboardButton("↩️ indietro",
                                        callback_data=Reservation())]

        reply_markup = InlineKeyboardMarkup(build_menu(
            keyboard, n_cols=7, header_buttons=header, footer_buttons=footers))

        text_reply = f"seleziona data"
        return text_reply, reply_markup

    @classmethod
    def confirm_reservation_action(
        cls,
        the_reservation: Reservation
    ) -> tuple[str, InlineKeyboardMarkup]:
        text_reply = f"Riepilogo prenotazione:\n \
            posti prenotati: {the_reservation.reserved_seats}\n \
            data: {the_reservation.reservation_date}\n \
            fascia oraria: {the_reservation.time_period}\n\n \
            vuoi confermare la prenotazione?"

        object_copy = copy.deepcopy(the_reservation)
        object_copy.time_period = None
        the_reservation.is_reservation_ready = True
        keyboard = [
            InlineKeyboardButton("conferma",
                                callback_data=the_reservation),
            InlineKeyboardButton("↩️ indietro",
                                callback_data=object_copy)
        ]
        reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))

        return text_reply, reply_markup

    @classmethod
    def end_reservation_action(
        cls,
        reservation_has_succeed: bool,
        reservation_list: List[dict]
    ) -> tuple[str, InlineKeyboardMarkup]:
        keyboard = [
            InlineKeyboardButton("Nuova prenotazione",
                                callback_data=Reservation())]

        if reservation_has_succeed:
            text_reply = f"prenotazione confermata!\nOra scegli se effettuare una nuova prenotazione o ritornare al menu principale!"
            keyboard.append(InlineKeyboardButton("Le mie prenotazioni",
                                                callback_data=Gallery(the_class=Reservation, the_query=reservation_list)))
        else:
            text_reply = f"la prenotazione non ha avuto successo\nEffettua per piacere una nuova prenotazione oppure torna al menu principale"

        keyboard.append(InlineKeyboardButton("menu principale 🏠",
                                            callback_data='menu_principale'))

        reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))

        return text_reply, reply_markup

    @classmethod
    def office_selection(
        cls,
        the_reservation: Reservation,
        office_list: dict,
        role_authorization: dict # da aggiungere controllo autorizzazioni per vari uffici
    ) -> tuple[str, InlineKeyboardMarkup]:
        keyboard = []
        for i in office_list:
            object_copy = copy.deepcopy(the_reservation)
            object_copy.office_name = i["OfficeName"]
            object_copy.office_total_seats = i["TotalSeats"]
            keyboard.append(InlineKeyboardButton(i["OfficeName"],
                                                callback_data=object_copy))
            keyboard.append(InlineKeyboardButton("ℹ️",
                                                callback_data=f"info_{i['Description']}"))

        footer = InlineKeyboardButton("↩️ indietro",
                                    callback_data="menu_prenotazioni")

        reply_markup = InlineKeyboardMarkup(build_menu(
            keyboard, n_cols=2, footer_buttons=footer))
        text_reply = f"Seleziona l'ufficio che ti serve:"

        return text_reply, reply_markup
    
    @classmethod    
    def seats_interface(
        cls,
        the_reservation: Reservation,
        role_authorization: dict
    ) -> tuple[str, InlineKeyboardMarkup]:
        office_total_seats = the_reservation.office_total_seats
        max_seats_user_can_reserve = N_POSTIPRENOTABILI
        if role_authorization["AuthorizationLevel"] <= AUTH_MAXPOSTIPRENOTABILI:
            max_seats_user_can_reserve = office_total_seats

        keyboard = []
        for seat in range(1, max_seats_user_can_reserve+1):
            object_copy = copy.deepcopy(the_reservation)

            object_copy.reserved_seats = seat
            keyboard.append(InlineKeyboardButton(seat,
                                                callback_data=object_copy))

        for empty_button in range(8 - max_seats_user_can_reserve % 8):
            keyboard.append(InlineKeyboardButton(" ",
                                                callback_data=the_reservation))

        object_copy = copy.deepcopy(the_reservation)
        object_copy.office_name= None
        footers = [InlineKeyboardButton("↩️ indietro",
                                        callback_data=object_copy)]

        reply_markup = InlineKeyboardMarkup(build_menu(keyboard,
                                                    n_cols=8,
                                                    footer_buttons=footers))
        text_reply = f"Seleziona posti da prenotare:"

        return text_reply, reply_markup

    @classmethod
    def show_reservation_list_action(
        cls,
        the_gallery: Gallery
    ) -> tuple[str, InlineKeyboardMarkup]:

        str_back_action = "⬅️"
        str_next_action = "➡️"
        gallery_object_back_action = copy.deepcopy(the_gallery)
        gallery_object_next_action = copy.deepcopy(the_gallery)
        gallery_object_delete_action = copy.deepcopy(the_gallery)
        gallery_object_delete_action.user_want_to_delete_change()
        keyboard = []
        gallery_object_back_action.back()
        gallery_object_next_action.next()
        
        if the_gallery.pos == 0:
            str_back_action = " "
        if the_gallery.pos == the_gallery.size-1:
            str_next_action = " "
        if not( str_back_action == " " and str_next_action == " "):
            keyboard = [
            InlineKeyboardButton(str_back_action,
                                callback_data=gallery_object_back_action),
            InlineKeyboardButton(str_next_action,
                                callback_data=gallery_object_next_action)]

        

        keyboard.append(InlineKeyboardButton("cancella",
                                callback_data=gallery_object_delete_action))
        

        footers = [InlineKeyboardButton("↩️ indietro",
                                        callback_data="menu_prenotazioni")]
        text_reply = the_gallery.show()
        reply_markup = InlineKeyboardMarkup(build_menu(keyboard,
                                                    n_cols=2,
                                                    footer_buttons=footers))

        return text_reply, reply_markup

    @classmethod
    def delete_reservation_action(
        cls,
        the_gallery: Gallery
    ) -> tuple[str, InlineKeyboardMarkup]:

        gallery_object_abort_action = copy.deepcopy(the_gallery)
        gallery_object_confirm_action = copy.deepcopy(the_gallery)
        gallery_object_abort_action.user_want_to_delete_change()
        gallery_object_confirm_action.is_ready_to_delete_change()

        keyboard = [
            InlineKeyboardButton("annulla",
                                callback_data=gallery_object_abort_action),
            InlineKeyboardButton("conferma",
                                callback_data=gallery_object_confirm_action)
        ]

        reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=2))

        text_reply = f"{the_gallery.show()}\nSei sicuro di cancellare questa prenotazione?"
        return text_reply, reply_markup

    @classmethod
    def confirm_delete_action(
        cls,
        the_gallery: Gallery
    ) -> tuple[str, InlineKeyboardMarkup]:

        keyboard = []

        if the_gallery.delete():
            text_reply = "Prenotazione cancellata con successo!\nOra scegli se tornare alle tue prenotazioni o al menu"
        else:
            text_reply = "Purtroppo non siamo riusciti a cancellare la tua prenotazione, contatta la segreteria per ottenere ulteriore supporto"

        if the_gallery.size > 0:
            keyboard.append(InlineKeyboardButton("le mie prenotazioni",
                                                callback_data=the_gallery))

        keyboard.append(InlineKeyboardButton("menu principale",
                                            callback_data="menu_principale"))

        reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=1))

        return text_reply, reply_markup

    @classmethod
    def delete_profile_action(
        cls
    ):
        text_reply = "Sei sicuro di cancellare tutti i dati che detiene il bot, ovvero i dati di sistema, i contatti e le prenotazioni?"
        keyboard = [
            InlineKeyboardButton("annulla",
                                callback_data="menu_profilo"),
            InlineKeyboardButton("conferma",
                                callback_data="cancella_dati")
        ]

        reply_markup = InlineKeyboardMarkup(build_menu(keyboard, n_cols=2))

        return text_reply, reply_markup

    @classmethod
    def change_contacts_action(
        cls
    ) -> tuple[str, InlineKeyboardMarkup]:
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

