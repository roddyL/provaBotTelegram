import datetime as dt
from typing import List

class Prenotazione():

    def __init__(self) -> None:
        self.seats = None # posti necessari per l'utente
        self.datetime = None # giorno prenotazione
        self.hours = None  # fascia oraria
        self.name = None # nome utente
        self.surname = None # cognome utente
        self.phoneNumber = None # numero cellulare utente
        self.mail = None # mail utente
        self.username = None # username telegram utente

    def __repr__(self):
        return f"seats: {self.seats} \ndatetime: {self.datetime} \nhours: {self.hours} \nname: {self.name} \nsurname: {self.surname} \nphoneNumber: {self.phoneNumber} \nmail: {self.mail}"

    def check_occupati(self) -> List[dt.date]:
        pass
    
    def setSeats(self, seats: int):
        self.seats=seats

    def setDatetime(self, datetime: dt.date):
        self.datetime=datetime

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

    def carica_prenotazione(self, username: str) -> bool:
        query=""
        pass

    def conferma(self, username: str) -> bool:
        if self.seats and self.datetime and self.hours and self.name and self.surname and self.phoneNumber and self.mail:    
            if self.carica_prenotazione(username):
                return True
        return False
    
    def continua_prenotazione(self) -> None:
        pass
    # def continua_prenotazione(self):
    #     if not self.conferma("si"):
    #         return False
    #     elif not self.seats:
    #         self.seats(12)
    #     elif not self.datetime:
    #         self.datetime(dt.date(2022,9,12))
    #     elif not self.hours:
    #         self.hours("mattino")
    #     elif not self.name:
    #         self  


nuova=Prenotazione()

    
print(nuova)
print(nuova.conferma("si"))

