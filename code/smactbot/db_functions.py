# db_functions.py

# import delle librerie
from ast import Return
import datetime
import pymysql as mc
from typing import List

from smactbot.utils.utility import check_contacts, create_idPrenotazione

def insert_whitelist(
    telegram_id: int
) -> None:
    """insert_whitelist()
    
    La funzione inserisce nel database lo username dell'utente che ha effettuato il log in, solo se non era presente nella whitelist.

    Args:
        username (str): username da inserire nella whitelist
    """
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(
                f"INSERT INTO `whitelist` (`telegram_id`,`dt_lastLogin`) VALUES ({telegram_id},CURRENT_TIMESTAMP)")
            __myconn.commit()

def check_whitelist(
    already_logged: bool = False
) -> List[str]:
    """check_whitelist()

    La funzione va a prendere la lista di persone che hanno già fatto il log in nel sistema.
    Si può cambiare il campo booleano already_logged per ricevere la lista di persone che sono ancora loggate
    oppure per ricevere la lista dei log delle persone che hanno fatto il log in, ma la cui sessione è scaduta.

    Args:
        already_logged (bool, optional): True controllerà le sessioni degli utenti nella whitelist, 
        False controllerà gli utenti già presenti nella whitelist. Defaults to False.

    Returns:
        List[str]: utenti presenti nella whitelist
    """
    if already_logged:
        logged = 0
    else:
        logged = 1
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        # update whitelist da database
        with __myconn.cursor() as cur:
            cur.execute(f"select * from whitelist where is_logged={logged}")
            whitelist = [i["telegram_id"] for i in cur.fetchall()]

    return whitelist

def update_session(
    telegram_id: int
) -> None:
    """update_session()

    La funzione rende possibile fare l'update dell'ultimo log in dell'utente

    Args:
        username (str): utente che deve aggiornare la sessione
    """
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(
                f"UPDATE `whitelist` SET is_logged=1, dt_lastLogin=CURRENT_TIMESTAMP WHERE telegram_id={telegram_id}")
            __myconn.commit()

def logout(
    telegram_id: int
) -> None:
    """logout()

    La funzione rende possibile togliere il log in alla persona senza cancellarla dal database

    Args:
        username (str): utente che deve effettuare il logout
    """
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(
                f"UPDATE `whitelist` SET is_logged=0 WHERE telegram_id={telegram_id}")
            __myconn.commit()

def insert_prenotazione(
    telegram_id: int, 
    seats: int, 
    the_datetime: datetime.date, 
    hours: str,
    nome_ufficio: str = 'liveDemo+9' 
) -> bool:
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(f"select id_prenotazione from prenotazione where data='{the_datetime}' order by id desc LIMIT 1")
            print()
            n_incremental=cur.fetchall()
            if not n_incremental:
                n_incremental=0
            else:
                n_incremental=int(n_incremental[0]["id_prenotazione"].split("_")[1])
                print(n_incremental)
            
            idPrenotazione=create_idPrenotazione(the_datetime=the_datetime, n_incremental=n_incremental)
            if not hours=="intera giornata":
                query=f"INSERT INTO `prenotazione` (`id_prenotazione`, `telegram_id`, `nome_ufficio`, `posti_prenotati`, `fascia_oraria`, `data`, `timestamp`)\
                        VALUES  ('{idPrenotazione}', '{telegram_id}', '{nome_ufficio}', '{seats}', '{hours}', '{the_datetime}',  current_timestamp())"
            else:
                query=f"INSERT INTO `prenotazione` (`id_prenotazione`, `telegram_id`, `nome_ufficio`, `posti_prenotati`, `fascia_oraria`, `data`, `timestamp`)\
                        VALUES  ('{idPrenotazione}', '{telegram_id}', '{nome_ufficio}', '{seats}', 'mattino', '{the_datetime}',  current_timestamp()),\
                                ('{idPrenotazione}', '{telegram_id}', '{nome_ufficio}', '{seats}', 'pomeriggio', '{the_datetime}',  current_timestamp())"
            
            try:
                result=cur.execute(query)
                if result==0 or (result==1 and hours=="intera giornata"):
                    return False
                else:
                    __myconn.commit()
                    return True    
            except Exception as e:
                print(e)
                return False
                    

def check_busyDays(
    posti_daPrenotare: int,
    monthSelected: datetime.date
) -> List[datetime.date]:
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(f"select `p`.`data` AS `data`,`u`.`posti` - sum(`p`.`posti_prenotati`) AS `posti_disponibili` \
                            from (`tg_bot`.`prenotazione` `p` join `tg_bot`.`ufficio` `u` on(`p`.`nome_ufficio` = `u`.`nome_ufficio`)) \
                            WHERE MONTH(p.data)=MONTH('{monthSelected}')\
                            group by `p`.`data`, p.fascia_oraria\
                            HAVING posti_disponibili<{posti_daPrenotare};")
            busy_days = [i["data"] for i in cur.fetchall()]
            busy_days= [i for i in busy_days if busy_days.count(i)>1]
    
    return busy_days

def check_busyHours(
    data: datetime.date,
    posti_daPrenotare: int
) -> List[str]:
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(f"select p.fascia_oraria, `u`.`posti` - sum(`p`.`posti_prenotati`) AS `posti_disponibili` \
                            from (`tg_bot`.`prenotazione` `p` join `tg_bot`.`ufficio` `u` on(`p`.`nome_ufficio` = `u`.`nome_ufficio`)) \
                            WHERE p.data='{data}'\
                            GROUP BY p.fascia_oraria\
                            HAVING posti_disponibili<{posti_daPrenotare};")
            busy_hours = [i["fascia_oraria"] for i in cur.fetchall()]

    return busy_hours

def return_auth(telegram_id) -> int:
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(f"select r.livello_permesso \
                from ruolo as r inner join utente as u on r.nome_ruolo=u.nome_ruolo \
                where u.telegram_id={telegram_id}")
        return cur.fetchone()["livello_permesso"]

def auth(nome_ruolo) -> int:
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(f"select r.livello_permesso \
                from ruolo as r \
                where nome_ruolo='{nome_ruolo}'")
        return cur.fetchone()["livello_permesso"]


def insert_firstStart(
    telegram_id: int,
    username: str=None
):
        query=f"INSERT INTO `utente` (`telegram_id`, `Username`,`nome_ruolo`) VALUES ({telegram_id},'{username}','guest')"
        with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
            with __myconn.cursor() as cur:
                try:
                    cur.execute(query)
                except Exception as e:
                    return     
                
                __myconn.commit()
                

def insert_contacts(
    telegram_id: int,
    username: str,
    contatti: str
):
    if check_contacts(contatti):
        
        # inserire query per il database
        cont=contatti.split("\n")
        query=f"UPDATE `utente` SET `Nome`='{cont[0]}', `Cognome`='{cont[1]}', `Recapito_telefonico`='{cont[2]}', `Mail`='{cont[3]}' WHERE `telegram_id`={telegram_id}"
        with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
            with __myconn.cursor() as cur:
                cur.execute(query)
                __myconn.commit()
        
        insert_whitelist(telegram_id)

        return True
    else:
        return False
    
def change_role(
    telegram_id: int,
    nome_ruolo: str
):
    query=f"UPDATE `utente` SET `nome_ruolo`='{nome_ruolo}' WHERE `telegram_id`={telegram_id}"
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(query)
            __myconn.commit()

def show_contacts(
    telegram_id: int
) -> str:
    query=f"SELECT Nome, Cognome, Recapito_telefonico, Mail FROM `utente` where telegram_id={telegram_id}"
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(query)
            contatti=cur.fetchall()[0]
            return f"{contatti['Nome']}\n{contatti['Cognome']}\n{contatti['Recapito_telefonico']}\n{contatti['Mail']}"

def show_prenotazioni(
    telegram_id: int
) -> str:
    query=f"SELECT * \
            FROM (\
                SELECT id_prenotazione, nome_ufficio, posti_prenotati, 'intera giornata' as fascia_oraria, data, timestamp \
                FROM `prenotazione` \
                where telegram_id={telegram_id} \
                group by id_prenotazione \
                having count(*)>1 \
            UNION \
                SELECT  id_prenotazione, nome_ufficio, posti_prenotati, fascia_oraria, data, timestamp \
                FROM `prenotazione` \
                where telegram_id={telegram_id} \
                group by id_prenotazione \
                having count(*)=1) as a \
            where data>={datetime.date.today()}\
            order by a.id_prenotazione;"

    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(query)
            prenotazioni=cur.fetchall()
            if len(prenotazioni)>0:
                return prenotazioni
            else:
                False

def delete_prenotazione(
    id_prenotazione: str
) -> bool:
    query=f"delete from prenotazione where id_prenotazione='{id_prenotazione}'"
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            if cur.execute(query):
                __myconn.commit()
                return True
            else:
                return False
    