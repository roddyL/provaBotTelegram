# !/code/smactbot/models/Reservation.py
# Authors:
#     Alberto
#     Loris

# libraries
import datetime as dt
from smactbot.db_functions import insert_reservation, delete_reservation

# the class Reservation
class Reservation():
    """This class contains all the informations about a reservation. 
    This reservation is meant to be uploaded on the db. The methods
    inside allows an easier upload and management of the reservation.
    """
    
    def __init__(self) -> None:
        self.reservation_id = None 
        """Str: date_id \nFor example: 2022-12-22_1"""
        self.telegram_id = None
        """Int: the telegram user id"""
        self.office_name = None
        """Str: name of the office selected"""
        self.reserved_seats = None
        """Int: number of seats that user has been reserved"""
        self.office_total_seats = None
        """Int: the max possible number of seats in the office"""
        self.reservation_date = None
        """Datetime.date: date selected by the user for the reservation"""
        self.next_month_to_show = None
        """Datetime.date: the next month that will be showed in the 
        calendar interface"""
        self.showed_month = dt.date.today()
        """Datetime.date: the month that is showed in the calendar
        interface. Default is the month of today"""
        self.time_period = None
        """Str: the time period selected by the user. For example:
        'Morning', 'Afternoon' or 'the entire day'"""
        self.is_reservation_ready = False
        """Bool: until the user don't press the confirm button, the var 
        is set to False, insted when it press the button the reservation
        is ready and the upload will initialize"""


    def gallery_item_constructor(self, tupla: dict) -> object:
        """From a tuple of the db, it creates a reservation with the 
        info inside the tuple

        Args:
            tupla (dict): the tuple came from the db

        Returns:
            object: return itself
        """
        self.reservation_id = tupla['ReservationId']
        self.telegram_id = None
        self.office_name = tupla['OfficeName']
        self.reserved_seats = int(tupla['ReservedSeats'])
        self.office_total_seats = int(tupla['TotalSeats'])
        self.reservation_date = tupla['ReservationDate']
        self.time_period = tupla['TimePeriod']
        self.next_month_to_show = None
        self.showed_month = dt.date.today()
        self.is_reservation_ready = True
        return self


    def __repr__(self):
        return f"\nReserved seats: {self.reserved_seats} \n\
                Reserved date: {self.reservation_date} \n\
                Reserved time period: {self.time_period}"


    def upload_reservation(self, telegram_id: str) -> bool:
        """It uploads the reservation on the db, passing
        - telegram_id
        - reserved_seats
        - reservation_date
        - time_period
        - office_name

        Args:
            telegram_id (str): the unique identifier number of the user

        Returns:
            bool: True if it has worked, False otherwise
        """
        return insert_reservation(telegram_id=telegram_id,
                                  reserved_seats=self.reserved_seats,
                                  reservation_date=self.reservation_date,
                                  time_period=self.time_period,
                                  office_name=self.office_name)


    def confirm_reservation(self, telegram_id: str) -> bool:
        """It checks if the fields are filled, than it uploads
        with the method upload_reservation()

        Args:
            telegram_id (str): the unique identifier number of the user

        Returns:
            bool: True if it has worked, False otherwise
        """
        if self.office_name and self.reserved_seats and self.reservation_date and self.time_period:
            return self.upload_reservation(telegram_id)
        else:
            return False

    # def aggiorna(self, telegram_id: str) -> bool:
    #     if self.reserved_seats and self.reservation_date and self.time_period:
    #         if self.upload_reservation(telegram_id):
    #             return True

    #     return False

    def show_to_gallery(self) -> str:
        """It gives the info about the reservation for the Gallery
        
        Returns:
            str: ready to print, with fields:
            - Reservation
            - Office name
            - Reservation date
            - Time period
            - Reserved seats
        """
        return f"Reservation: {self.reservation_id}\n\
            Office name: {self.office_name}\n\
            Reservation date: {self.reservation_date}\n\
            Time period: {self.time_period}\n\
            Reserved_seats: {self.reserved_seats}"

    def delete_reservation(self) -> bool:
        """It deletes the reservation from the db

        Returns:
            bool: True if it has worked, False otherwise
        """
        return delete_reservation(reservation_id=self.reservation_id)
