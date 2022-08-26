import datetime as dt
from typing import List

class Prenotazione():

    def __init__(self) -> None:
        self.seats = None # posti necessari per l'utente
        self.the_datetime = None # giorno prenotazione
        self.hours = None  # fascia oraria
        self.telegram_id = None # telegram_id utente
        self.chMonth=None # cambiare mese corrente

    def __repr__(self):
        return f"\nseats: {self.seats} \ndatetime: {self.the_datetime} \nhours: {self.hours}"

    def getSeats(self):
        return self.seats

    def setSeats(self, seats: int):
        self.seats=seats

    def setChMonth(self, chMonth: dt.date):
        self.chMonth=chMonth

    def setDatetime(self, the_datetime: dt.date):
        self.the_datetime=the_datetime

    def setHours(self, hours: str):
        self.hours=hours

    def carica_prenotazione(self, telegram_id: str) -> bool:
        query=""
        pass

    def conferma(self, telegram_id: str) -> bool:
        if self.seats and self.the_datetime and self.hours:    
            if self.carica_prenotazione(telegram_id):
                return True
        return False
    
