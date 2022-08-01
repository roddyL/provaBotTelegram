# db_functions.py

import pymysql as mc
from typing import List

def insert_whitelist(
    username: str
) -> None:
    """insert_whitelist()

    Args:
        username (str): username da inserire nella whitelist
    """
    with mc.connect(host="localhost",user = "root", passwd="",database="tg_bot",cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(f"INSERT INTO `whitelist` (`username`,`dt_lastLogin`) VALUES ('{username}',CURRENT_TIMESTAMP)")
            __myconn.commit()

def check_whitelist(
    already_logged: bool=False
) -> List[str]:
    """check_whitelist()

    Args:
        already_logged (bool, optional): True controllerà le sessioni degli utenti nella whitelist, 
        False controllerà gli utenti già presenti nella whitelist. Defaults to False.

    Returns:
        List[str]: utenti presenti nella whitelist
    """
    if already_logged:
        logged=0
    else:
        logged=1
    with mc.connect(host="localhost",user = "root", passwd="",database="tg_bot",cursorclass=mc.cursors.DictCursor) as __myconn:
        # update whitelist da database
        with __myconn.cursor() as cur: 
            cur.execute(f"select * from whitelist where is_logged={logged}")
            whitelist=[i["username"] for i in cur.fetchall()]

    return whitelist

def update_session(
    username: str
) -> None:
    """update_session()

    Args:
        username (str): utente che deve aggiornare la sessione
    """
    with mc.connect(host="localhost",user = "root", passwd="",database="tg_bot",cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(f"UPDATE `whitelist` SET is_logged=1, dt_lastLogin=CURRENT_TIMESTAMP WHERE username='{username}'")
            __myconn.commit()

def logout(
    username: str
) -> None:
    """logout()

    Args:
        username (str): utente che deve effettuare il logout
    """
    with mc.connect(host="localhost",user = "root", passwd="",database="tg_bot",cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            cur.execute(f"UPDATE `whitelist` SET is_logged=0 WHERE username='{username}'")
            __myconn.commit()
