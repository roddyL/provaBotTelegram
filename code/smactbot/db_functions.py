# db_functions.py

# import delle librerie
import datetime
import pymysql as mc
from typing import List
from smactbot.queries import *

from smactbot.utils.utility import check_the_contact, create_reservation_id

def insert_whitelist(
    telegram_id: int
) -> None:
    """insert_whitelist()
    
    La funzione inserisce nel database ...

    Args:
        telegram_id (int): ...
    """
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(query_insert_whitelist.format(**locals()))
            __myconn.commit()

def check_whitelist(
    telegram_id: int
) -> List[str]:

    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        # update whitelist da database
        with __myconn.cursor() as cur:
            is_logged=None
            if cur.execute(query_check_whitelist.format(**locals())):
                is_logged=cur.fetchone()["IsLogged"]

    return is_logged

def update_session(
    telegram_id: int
) -> None:
    """update_session()

    La funzione rende possibile fare l'update dell'ultimo log in dell'utente

    Args:
        telegram_id (int): utente che deve aggiornare la sessione
    """
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(query_update_session.format(**locals()))
            __myconn.commit()

def logout(
    telegram_id: int
) -> None:
    """logout()

    La funzione rende possibile togliere il log in alla persona senza cancellarla dal database

    Args:
        telegram_id (int): utente che deve effettuare il logout
    """
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(query_logout.format(**locals()))
            __myconn.commit()

def get_role_password():
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            if cur.execute(query_get_role_password):
                result=cur.fetchall()
                passRuolo={i["Password"]:i["RoleName"] for i in result}
            else:
                passRuolo=False
    
    return passRuolo

def insert_reservation(
    telegram_id: int, 
    reserved_seats: int, 
    reservation_date: datetime.date, 
    time_period: str,
    office_name: str
) -> bool:
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(query1_insert_reservation.format(**locals()))
            n_incremental=cur.fetchall()
            if not n_incremental:
                n_incremental=0
            else:
                n_incremental=int(n_incremental[0]["ReservationId"].split("_")[1])
                print(n_incremental)
            
            reservation_id=create_reservation_id(reservation_date=reservation_date, n_incremental=n_incremental)
            print(reservation_id)
            try:
                
                if not time_period=="intera giornata":
                    print("qui")
                    # result=cur.execute(query2_insert_reservation.format(**locals()))
                    result=cur.execute(f"INSERT INTO `reservation` (`ReservationId`, `TelegramId`, `OfficeName`, `ReservedSeats`, `TimePeriod`, `ReservationDate`) VALUES  ('{reservation_id}', {telegram_id}, '{office_name}', '{reserved_seats}', '{time_period}', '{reservation_date}')"
)
                else:
                    print("qui")
                    result=cur.execute(query3_insert_reservation.format(**locals()))
                if result==0 or (result==1 and time_period=="intera giornata"):
                    return False
                else:
                    __myconn.commit()
                    return True
            except Exception as e:
                print(e)
                print("questo è l'errore")
                return False
                
def get_office(
) -> dict:
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(query_get_office)
            offices = cur.fetchall()
    
    return offices
                       

def check_busy_days(
    reserved_seats: int,
    selected_month: datetime.date,
    office_name: str
) -> List[datetime.date]:
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(query_check_busy_days.format(**locals()))
            busy_days = [i["ReservationDate"] for i in cur.fetchall()]
            busy_days = [i for i in busy_days if busy_days.count(i)>1]
    
    return busy_days

def check_busy_time_period(
    reservation_date: datetime.date,
    reserved_seats: int,
    office_name: str
) -> List[str]:
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(query_check_busy_time_period.format(**locals()))
            busy_hours = [i["TimePeriod"] for i in cur.fetchall()]

    return busy_hours

def check_authorization(telegram_id) -> dict:
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(query_check_authorization.format(**locals()))
            result = cur.fetchone()
    return result

def insert_first_start(
    telegram_id: int,
    username: str=None
) -> None:
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            if not cur.execute(query1_insert_first_start.format(**locals())):
                cur.execute(query2_insert_first_start.format(**locals()))
                __myconn.commit()
                

def insert_contacts(
    telegram_id: int,
    contact_type: str,
    the_single_contact: str
):
    if check_the_contact(contact_type=contact_type, the_single_contact=the_single_contact):
        with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
            with __myconn.cursor() as cur:
                result=cur.execute(query_insert_contacts.format(**locals()))
                __myconn.commit()

        return result>0
    else:
        return False
    
def change_role(
    telegram_id: int,
    role_name: str
):
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(query_change_role.format(**locals()))
            __myconn.commit()

def show_contacts(
    telegram_id: int
) -> str:
    
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(query_show_contacts.format(**locals()))
            contacts=cur.fetchone()
            output=""
            for i in contacts.values():
                if i:
                    output+=f"{i}\n"
            return output

def show_reservations(
    telegram_id: int
) -> dict:
    

    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            today = datetime.date.today()
            cur.execute(query_show_reservations.format(**locals(),**globals()))
            reservations=cur.fetchall()
            if len(reservations)>0:
                return reservations
            else:
                False

def delete_reservation(
    reservation_id: str
) -> bool:
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            if cur.execute(query_delete_reservation.format(**locals())):
                __myconn.commit()
                return True
            else:
                return False

def delete_data(
    telegram_id: int
) -> bool:
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            if cur.execute(query_delete_data.format(**locals())):
                __myconn.commit()
                return True
            else:
                return False