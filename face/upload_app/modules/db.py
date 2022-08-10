# Get an instance of a logger

import datetime
import pymysql.cursors
import pymysql


CONNECT_AUTH_BASE = "None"   # Для авторизации в базе данных


def active_code(code):
    """ Функция обращения к базе данных. \n
    Code = FInviteCode (код допуска). \n
    функция одноканальная с переавторизацией.
    """
    global CONNECT_AUTH_BASE

    # Connect to the database
    if CONNECT_AUTH_BASE == "None":
        CONNECT_AUTH_BASE = pymysql.connect(host='192.168.48.114',
                                     user='Nik',
                                     password='1234567',
                                     db='sac3',
                                     charset='cp1251',
                                     cursorclass=pymysql.cursors.DictCursor)

    # cp1251
    try:
        with CONNECT_AUTH_BASE.cursor() as cur:
            # отправляем запрос базе
            
            cur.execute(f"select * from tguest where FInviteCode like {code} and FDateFrom < GETDATE() < FDateTo")

            result = cur.fetchall()  # выгружаем данные из запроса
            name = f'{result[0]["FLastName"]} {result[0]["FFirstName"]} {result[0]["FMiddleName"]}'
            
            id = result[0]['FID']
            active = True
            CONNECT_AUTH_BASE.commit()
            return active, id, name

    except pymysql.OperationalError as e:
        return False, "0", "0"
    except Exception as ex:
        CONNECT_AUTH_BASE = "None"
        print(ex)
        return False, "0", "0"
