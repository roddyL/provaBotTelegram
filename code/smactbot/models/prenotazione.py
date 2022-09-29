import datetime as dt
from typing import List
from smactbot.db_functions import insert_prenotazione, delete_prenotazione

class Prenotazione():

    def __init__(self) -> None:
        self.seats = 1 # posti necessari per l'utente
        self.maxSeats = None
        self.seatsReady = False
        self.the_datetime = None # giorno prenotazione
        self.hours = None  # fascia oraria
        self.telegram_id = None # telegram_id utente
        self.chMonth=None # cambiare mese corrente
        self.monthSelected=dt.date.today()
        self.ready=False
        self.idPrenotazione=None
        self.nome_ufficio=None
        self.timestamp=None
        self.isUpdating=None

    def costruttore(self, tupla: dict) -> object:
        self.seats=int(tupla['posti_prenotati'])
        self.maxSeats=int(tupla['posti'])
        self.seatsReady=True
        self.the_datetime=tupla['data']
        self.hours=tupla['fascia_oraria']
        self.telegram_id = None
        self.chMonth=None
        self.monthSelected=dt.date.today()
        self.ready=True
        self.idPrenotazione=tupla['id_prenotazione']
        self.nome_ufficio=tupla['nome_ufficio']
        self.timestamp=tupla['timestamp']
        return self

    def __repr__(self):
        return f"\nseats: {self.seats} \ndatetime: {self.the_datetime} \nhours: {self.hours}"

    def getSeats(self):
        return self.seats

    def setUfficio(self, nome_ufficio: str):
        self.nome_ufficio=nome_ufficio

    def setSeats(self, seats: int):
        self.seats=seats
        
    def setMaxSeats(self, maxSeats: int):
        self.maxSeats=maxSeats
    
    def setSeatsReady(self, seatsReady: bool):
        self.seatsReady=seatsReady

    def setMonthSelected(self, monthSelected: dt.date):
        self.monthSelected=monthSelected

    def setChMonth(self, chMonth: dt.date):
        self.chMonth=chMonth

    def setDatetime(self, the_datetime: dt.date):
        self.the_datetime=the_datetime

    def setHours(self, hours: str):
        self.hours=hours
        
    def setReady(self, ready: bool):
        self.ready=True
    
    def setUpdating(self, isUpdating: bool):
        self.isUpdating=True

    def carica_prenotazione(self, telegram_id: str) -> bool:
        return insert_prenotazione(telegram_id, self.seats, self.the_datetime, self.hours, self.nome_ufficio) 

    def conferma(self, telegram_id: str) -> bool:
        if self.seats and self.the_datetime and self.hours:    
            if self.carica_prenotazione(telegram_id):
                return True

        return False
    
    def aggiorna(self, telegram_id: str) -> bool:
        if self.seats and self.the_datetime and self.hours:
            if self.carica_prenotazione(telegram_id):
                return True

        return False

    def showToGallery(self) -> str:
        return f"Prenotazione: {self.idPrenotazione}\nufficio prenotato: {self.nome_ufficio}\ndata prenotazione: {self.the_datetime}\nnella fascia oraria: {self.hours}\nposti prenotati: {self.seats}"
        
    def deletePrenotazione(self):
        return delete_prenotazione(self.idPrenotazione)

