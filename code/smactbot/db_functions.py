# !/code/smactbot/db_functions.py
# Authors:
#     Alberto
#     Loris
"""This module contains all the functions that perform actions on the database"""

# libraries

import datetime
import pymysql as mc
from typing import List, Union
from smactbot.log import logger
from smactbot.queries import *
from smactbot.config import (
    DB_HOST,
    DB_USER,
    DB_PASSWORD,
    DB_NAME
)
from smactbot.utils.utility import (
    check_the_contact,
    create_reservation_id
)

# code


def generic_db_function(
    query: str,
    commit: bool = False
) -> Union[List[dict], bool]:
    """This is the base function to access the SQL database throught queries.
    It can sends and receive data.

    Args:
        query (str): accept only INSERT, UPDATE, DELETE and SELECT commands.
        commit (bool, optional): set True if you're doing INSERT, UPDATE or DELETE, 
            otherwise False. Defaults to False.

    Returns:
        Union[List[dict], bool]: In the case of a SELECT it returns a list of dict,
            otherwise it returns True if the query has affected rows, False if it hasn't.
    """
    with mc.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, database=DB_NAME, cursorclass=mc.cursors.DictCursor) as __myconn:
        with __myconn.cursor() as cur:
            try:
                result = cur.execute(query) > 0
                if not commit:
                    result = cur.fetchall()
                else:
                    __myconn.commit()
            except Exception as e:
                print(e)
                logger.error()
                return False

    return result


def insert_whitelist(
    telegram_id: int
) -> bool:
    """It inserts the user into the whitelist

    Args:
        telegram_id (int): the unique identifier number of the user

    Returns:
        bool: True if it has worked, False otherwise
    """
    return generic_db_function(query=query_insert_whitelist.format(**locals()),
                               commit=True)


def check_whitelist(
    telegram_id: int
) -> bool:
    """It check if the user is in the whitelist and is it logged

    Args:
        telegram_id (int): the unique identifier number of the user

    Returns:
        bool: True if the user is logged, False otherwise 
    """
    result = generic_db_function(
        query=query_check_whitelist.format(**locals()))
    if result:
        return result[0]["IsLogged"]
    else:
        return result


def update_session(
    telegram_id: int
) -> bool:
    """It does the update of the session of the user

    Args:
        telegram_id (int): the unique identifier number of the user

    Returns:
        bool: True if it has worked, False otherwise
    """
    return generic_db_function(query=query_update_session.format(**locals()),
                               commit=True)


def logout(
    telegram_id: int
) -> bool:
    """It does the logout of the user from the bot, 
    but all the data remains in the db.

    Args:
        telegram_id (int): the unique identifier number of the user

    Returns:
        bool: True if it has worked, False otherwise
    """
    return generic_db_function(query=query_logout.format(**locals()),
                               commit=True)


def get_role_password() -> dict:
    """It gives in pairs the Password and the associated Rolename.

    Returns:
        dict: keys are the password, values are the relative rolenames.
    """
    result = generic_db_function(query=query_get_role_password)
    if result:
        result = {role["Password"]: role["RoleName"] for role in result}

    return result


def insert_reservation(
    telegram_id: int,
    reserved_seats: int,
    reservation_date: datetime.date,
    time_period: str,
    office_name: str
) -> bool:
    """It create an identifier for the reservation using create_reservation_id(), then
    it insert the reservation in the db 

    Args:
        telegram_id (int): the unique identifier number of the user
        reserved_seats (int): number of seats selected by the user 
        reservation_date (datetime.date): the date selected by the user
        time_period (str): the time period selected by the user
        office_name (str): the office selected by the user

    Returns:
        bool: True if it has worked, False otherwise
    """

    # find the last reservation id from the day that has been selected (if it exists)
    n_incremental = generic_db_function(
        query=query1_insert_reservation.format(**locals())
    )
    if not n_incremental:
        # there is no reservations for the day that has been selected
        # so n_incremental has value 0 and the next id will be 1
        n_incremental = 0  
    else:
        # n_incremental take the value of the highest id of the day selected
        # so the next id will be n_incremental+1
        n_incremental = int(n_incremental[0]["ReservationId"].split("_")[1])

    # reservation_id = date_id
    # for example 2022-12-21_2
    reservation_id = create_reservation_id(
        reservation_date=reservation_date, n_incremental=n_incremental) 

    
    try:
        if not time_period == "intera giornata":
            result = generic_db_function(
                query=query2_insert_reservation.format(**locals()), commit=True)
        else:
            result = generic_db_function(
                query=query3_insert_reservation.format(**locals()), commit=True)

        return result > 0
    except Exception as e:
        print(e)
        return False


def get_office(
) -> dict:
    return generic_db_function(query=query_get_office)


def check_busy_days(
    reserved_seats: int,
    selected_month: datetime.date,
    office_name: str
) -> List[datetime.date]:
    result = generic_db_function(
        query=query_check_busy_days.format(**locals()))
    result = [day["ReservationDate"] for day in result]

    return [day for day in result if result.count(day) > 1]


def check_busy_time_period(
    reservation_date: datetime.date,
    reserved_seats: int,
    office_name: str
) -> List[str]:
    result = generic_db_function(
        query=query_check_busy_time_period.format(**locals()))

    return [time_period["TimePeriod"] for time_period in result]


def check_authorization(telegram_id) -> dict:
    result = generic_db_function(
        query=query_check_authorization.format(**locals()))

    return result[0]


def insert_first_start(
    telegram_id: int,
    username: str = None
) -> None:
    result = generic_db_function(
        query=query1_insert_first_start.format(**locals()))
    if not result:
        result = generic_db_function(
            query=query2_insert_first_start.format(**locals()), commit=True)

    return result


def insert_contacts(
    telegram_id: int,
    contact_type: str,
    the_single_contact: str
):
    if check_the_contact(contact_type=contact_type, the_single_contact=the_single_contact):
        result = generic_db_function(query=query_insert_contacts, commit=True)
        return result
    else:
        return False


def change_role(
    telegram_id: int,
    role_name: str
):
    result = generic_db_function(
        query=query_change_role.format(**locals()), commit=True)
    return result


def show_contacts(
    telegram_id: int
) -> str:
    result = generic_db_function(
        query=query_show_contacts.format(**locals()))[0]
    output = ""
    for i in result.values():
        if i:
            output += f"{i}\n"
    return output


def show_reservations(
    telegram_id: int
) -> dict:
    today = datetime.date.today()
    result = generic_db_function(
        query_show_reservations.format(**locals(), **globals()))

    return result


def delete_reservation(
    reservation_id: str
) -> bool:
    result = generic_db_function(
        query_delete_reservation.format(**locals()), commit=True)

    return result


def delete_data(
    telegram_id: int
) -> bool:
    result = generic_db_function(
        query_delete_data.format(**locals()), commit=True)

    return result
