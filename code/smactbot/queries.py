# !/code/smactbot/queries.py
# Authors:
#     Alberto
#     Loris
"""This module contains all the queries used in the module db_functions"""

# queries
query_insert_whitelist = "INSERT INTO `whitelist` (`TelegramId`,`DtLastLogin`) VALUES ({telegram_id},CURRENT_TIMESTAMP)"
query_check_whitelist = "select IsLogged from whitelist where TelegramId={telegram_id}"
query_update_session = "UPDATE `whitelist` SET IsLogged=1, DtLastLogin=CURRENT_TIMESTAMP WHERE TelegramId={telegram_id}"
query_logout = "UPDATE `whitelist` SET IsLogged=0 WHERE TelegramId={telegram_id}"
query_get_role_password = "select RoleName, Password from Role"
query1_insert_reservation = "select ReservationId from Reservation where ReservationDate='{reservation_date}' order by Id desc LIMIT 1"
query2_insert_reservation = "INSERT INTO `reservation` (`ReservationId`, `TelegramId`, `OfficeName`, `ReservedSeats`, `TimePeriod`, `ReservationDate`, `TimeStamp`)\
                        VALUES  ('{reservation_id}', '{telegram_id}', '{office_name}', '{reserved_seats}', '{time_period}', '{reservation_date}',  CURRENT_TIMESTAMP)"

query3_insert_reservation = "INSERT INTO `reservation` (`ReservationId`, `TelegramId`, `OfficeName`, `ReservedSeats`, `TimePeriod`, `ReservationDate`, `TimeStamp`)\
                        VALUES  ('{reservation_id}', '{telegram_id}', '{office_name}', '{reserved_seats}', 'mattino', '{reservation_date}',  CURRENT_TIMESTAMP),\
                                ('{reservation_id}', '{telegram_id}', '{office_name}', '{reserved_seats}', 'pomeriggio', '{reservation_date}',  CURRENT_TIMESTAMP)"
query_get_office = "select OfficeName, Description, TotalSeats from office"
query_check_busy_days = "select ReservationDate\
                        from empty_seats_v2\
                        WHERE MONTH(ReservationDate)=MONTH('{selected_month}') \
                        AND AvailableSeats<{reserved_seats} \
                        AND OfficeName='{office_name}'"
query_check_busy_time_period = "select TimePeriod\
                        from empty_seats_v2\
                        WHERE ReservationDate='{reservation_date}' \
                        AND AvailableSeats<{reserved_seats} \
                        AND OfficeName='{office_name}'"
query_check_authorization = "select r.RoleName, r.AuthorizationLevel \
                from role as r inner join user as u on r.RoleName=u.RoleName \
                where u.TelegramId={telegram_id}"
query1_insert_first_start="SELECT * from user where TelegramId='{telegram_id}'"
query2_insert_first_start = "INSERT INTO `user` (`TelegramId`, `Username`,`RoleName`) VALUES ({telegram_id},'{username}','guest')"
query_insert_contacts = "UPDATE `user` SET `{contact_type}`='{the_single_contact}' WHERE `TelegramId`={telegram_id}"
query_change_role = "UPDATE `user` SET `RoleName`='{role_name}' WHERE `TelegramId`={telegram_id}"
query_show_contacts = "SELECT Name, Surname, TelephoneNumber, Mail FROM `user` where TelegramId={telegram_id}"
query_show_reservations = "SELECT * \
                        FROM (\
                                SELECT ReservationId, OfficeName, ReservedSeats, 'intera giornata' as TimePeriod, ReservationDate, TimeStamp \
                                FROM `reservation`\
                                where TelegramId={telegram_id} \
                                group by ReservationId \
                                having count(*)>1 \
                        UNION \
                                SELECT ReservationId, OfficeName, ReservedSeats, TimePeriod, ReservationDate, TimeStamp \
                                FROM `reservation` \
                                where TelegramId={telegram_id} \
                                group by ReservationId \
                                having count(*)=1) as a inner join `office` as u on a.OfficeName=u.OfficeName\
                        where ReservationDate>={today}\
                        order by a.ReservationId;"
query_delete_reservation = "delete from reservation where ReservationId='{reservation_id}'"
query_delete_data = "delete from user where TelegramId={telegram_id}"