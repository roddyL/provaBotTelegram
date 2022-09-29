# db_functions.py

# import delle librerie
from ast import Return
import datetime
import pymysql as mc
from typing import List

from smactbot.utils.utility import check_the_contact, create_idPrenotazione

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
    telegram_id: int
    # already_logged: bool = False
) -> List[str]:
    # if already_logged:
    #     logged = 0
    # else:
    #     logged = 1
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        # update whitelist da database
        with __myconn.cursor() as cur:
            # cur.execute(f"select * from whitelist where is_logged={logged}")
            query=f"select is_logged from whitelist where telegram_id={telegram_id}"
            is_logged=None
            if cur.execute(query):
            # whitelist = [i["telegram_id"] for i in cur.fetchall()]
                is_logged=cur.fetchone()["is_logged"]

    return is_logged

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
            
def getPassword(
    nome_ruolo: str
) -> str:
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            
            if cur.execute(f"select password from ruolo where nome_ruolo='{nome_ruolo}'"):
                password=cur.fetchone()["password"]
            else:
                password=False
    
    return password

def getRuoli(
    nome_ruolo: str
) -> list[str]:
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            
            if cur.execute(f"select nome_ruolo from ruolo"):
                password=cur.fetchall()
            else:
                password=False
    
    return password

def getPassRuolo():
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            
            if cur.execute(f"select nome_ruolo, password from ruolo"):
                result=cur.fetchall()
                passRuolo={i["password"]:i["nome_ruolo"] for i in result}
            else:
                passRuolo=False
    
    return passRuolo

def insert_prenotazione(
    telegram_id: int, 
    seats: int, 
    the_datetime: datetime.date, 
    hours: str,
    nome_ufficio: str
) -> bool:
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(f"select id_prenotazione from prenotazione where data='{the_datetime}' order by id desc LIMIT 1")
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
 
def getUffici(

) -> dict:
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(f"select nome_ufficio, descrizione, posti from ufficio")
            uffici = cur.fetchall()
    
    return uffici
                       

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

def return_auth(telegram_id) -> dict:
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(f"select r.nome_ruolo, r.livello_permesso \
                from ruolo as r inner join utente as u on r.nome_ruolo=u.nome_ruolo \
                where u.telegram_id={telegram_id}")
        return cur.fetchone()

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
    tipo_contatto: str,
    il_contatto: str
):
    the_return=False
    if check_the_contact(tipo_contatto=tipo_contatto, il_contatto=il_contatto):
        
        # inserire query per il database

        query=f"UPDATE `utente` SET `{tipo_contatto}`='{il_contatto}' WHERE `telegram_id`={telegram_id}"
        with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
            with __myconn.cursor() as cur:
                if cur.execute(query):
                    __myconn.commit()
                    the_return=True
                
        
        # insert_whitelist(telegram_id)

        return the_return
    else:
        return the_return
    
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
            contatti=cur.fetchone()
            output=""
            for i in contatti.values():
                if i:
                    output+=f"{i}\n"
            return output

def show_prenotazioni(
    telegram_id: int
) -> dict:
    query=f"SELECT * \
            FROM (\
                SELECT id_prenotazione, nome_ufficio, posti_prenotati, 'intera giornata' as fascia_oraria, data, timestamp \
                FROM `prenotazione`\
                where telegram_id={telegram_id} \
                group by id_prenotazione \
                having count(*)>1 \
            UNION \
                SELECT  id_prenotazione, nome_ufficio, posti_prenotati, fascia_oraria, data, timestamp \
                FROM `prenotazione` \
                where telegram_id={telegram_id} \
                group by id_prenotazione \
                having count(*)=1) as a inner join `ufficio` as u on a.nome_ufficio=u.nome_ufficio\
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

def delete_data(
    telegram_id: int
) -> bool:
    query=f"delete from utente where telegram_id={telegram_id}"
    with mc.connect(host="localhost", user="root", passwd="", database="tg_bot", cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            if cur.execute(query):
                __myconn.commit()
                return True
            else:
                return False