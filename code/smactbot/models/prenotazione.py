import datetime as dt
from typing import List

class Prenotazione():

    def __init__(self) -> None:
        self.seats = None # posti necessari per l'utente
        self.the_datetime = None # giorno prenotazione
        self.hours = None  # fascia oraria
        self.name = None # nome utente
        self.surname = None # cognome utente
        self.phoneNumber = None # numero cellulare utente
        self.mail = None # mail utente
        self.username = None # username telegram utente
        self.listaPrenotati=None # persone prenotate
        self.chMonth=None # cambiare mese corrente

    def __repr__(self):
        return f"\nseats: {self.seats} \ndatetime: {self.the_datetime} \nhours: {self.hours} \nname: {self.name} \nsurname: {self.surname} \nphoneNumber: {self.phoneNumber} \nmail: {self.mail} \nlista prenotati: {self.listaPrenotati}"

    def getSeats(self):
        return self.seats

    def getListaPrenotati(self):
        return self.getListaPrenotati

    def setSeats(self, seats: int):
        self.seats=seats

    def setChMonth(self, chMonth: dt.date):
        self.chMonth=chMonth

    def setDatetime(self, the_datetime: dt.date):
        self.the_datetime=the_datetime

    def setHours(self, hours: str):
        self.hours=hours

    def setName(self, name: str):
        self.name=name

    def setSurname(self, surname: str):
        self.surname=surname

    def setPhoneNumber(self, phoneNumber: str):
        self.phoneNumber=phoneNumber

    def setMail(self, mail: str):
        self.mail=mail

    def setListaPrenotati(self, listaPrenotati: List):
        self.listaPrenotati=listaPrenotati

    def carica_prenotazione(self, username: str) -> bool:
        query=""
        pass

    def conferma(self, username: str) -> bool:
        if self.seats and self.the_datetime and self.hours and self.name and self.surname and self.phoneNumber and self.mail:    
            if self.carica_prenotazione(username):
                return True
        return False
    
