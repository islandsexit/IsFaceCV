# Get an instance of a logger

import datetime
import pymysql.cursors
import pymysql


CONNECT_AUTH_BASE = 'none'   # Для авторизации в базе данных


def active_code(code):
    """ Функция обращения к базе данных. \n
    Code = FInviteCode (код допуска). \n
    функция одноканальная с переавторизацией.
    """
    global CONNECT_AUTH_BASE

    # Connect to the database
    if CONNECT_AUTH_BASE == 'none':
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
            cur.execute(f"select * from tguest where FInviteCode like {code}")

            result = cur.fetchall()  # выгружаем данные из запроса

            time_from = result[0]['FDateFrom']
            time_to = result[0]['FDateTo']
            time_now = datetime.datetime.now().replace(microsecond=0)

            if time_from <= time_now <= time_to:  # Проверяем время допуска
                # обьеденяем имя фамилию отчество
                name = f'{result[0]["FLastName"]} {result[0]["FFirstName"]} {result[0]["FMiddleName"]}'
                id = result[0]['FID']
                active = True

                return active, id, name
            else:
                logger.error(str(datetime.datetime.now())+ ";[INFO];" + f"inactive code from db = {response_code}")
                return False, "0", "0"

    except Exception as ex:
        logger.error(str(datetime.datetime.now())+ ";[ERROR];" + f"code = {code} cannot connect to db server")
        return False, "0", "0"
