# import hashlib


# m = hashlib.sha256()
# a="fromfarmtofork"
# m.update(b"{a}")
# print(m.hexdigest())

# mi=hashlib.sha256()
# mi.update(b"fromfarmtofork")
# print(mi.hexdigest()==m.hexdigest())


month_enToIt={"January":"Gennaio","February":"Febbraio","March":"Marzo","April":"Aprile",
                "May":"Maggio","June":"Giugno","July":"Luglio","August":"Agosto","September":"Settembre",
                "October":"Ottobre","November":"Novembre","December":"Dicembre"}


import datetime
import calendar
from holidays import Italy as italianHolidays

def giorni_festivi(year: int):
    """_summary_

    Args:
        year (int): _description_
        month (str): mese da 

    Returns:
        List[datetime.date]: lista di giorni di ferie
    """
    festivi=[]
    for i, j in sorted(italianHolidays(subdiv="PD",years=year).items()):
        festivi.append(i)

    return festivi



# print(giorni_festivi(year=2022))
lista1=[1,2,3]
lista2=[4,5,6]
# print(lista1+lista2)
# print([i[-1] for i in calendar.monthcalendar(2022,8)])

# print(datetime.date.isocalendar(datetime.date.today()).weekday)
# print(datetime.date.today().day)
# print(datetime.date.today().month)
# print(datetime.date.today().year)

def strike(text):
    result = ''
    for c in text:
        result += c + '\u0336'
    return result

def italics(text):
    result = ''
    for c in text:
        result+= '\x1B[3m' + c 
    return result

def bold(text):
    result = ''
    for c in text:
        result += '\033[1m' + c 
    return result

def red(text):
    result = ''
    for c in text:
        result += '\033[91m' + c 
    return result


# print(strike("ciao a tutti son barrato"))
# print(bold("ciao a tutti son grassetto"))
# print(italics("ciao a tutti son corsivo"))
# print(red("ciao a tutti son red"))
 
print("next_11/2022"[:4])


# # print(calendar.monthcalendar(datetime.date.today().year,datetime.date.today().month))

# def dayInfo(day: datetime.date=datetime.date.today()) -> dict:
#     if not isinstance(day, datetime.date):
#         raise TypeError

#     giorni=[]
#     for i in calendar.monthcalendar(day.year,day.month):
#         for j in i:
#             if j==0:
#                 giorni.append(" ")
#             else:
#                 giorni.append(f"{j}")
#     return {strike("giorno"): day.day, "mese": month_enToIt[calendar.month_name[day.month]], "anno": day.year, "lista_giorni": giorni, "datetime": day}

# print(dayInfo())



# days=["Lu","Ma","Me","Gi","Ve","Sa","Do"]
# keyboard = [
#     f"{i}" for i in range(1,30)
# ]
# days+=keyboard

# print(days)
# print(keyboard)