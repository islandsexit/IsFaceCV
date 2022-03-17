import psycopg2
from psycopg2 import OperationalError
import json



def create_connection(db_name, db_user, db_password, db_host):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host
        )
    except OperationalError as e:
        print(f"Ошибка подключения к серверу '{e}'")
        return json.loads('{"Result":"ERROR", "DESC":"Ошибка подключения к серверу"}')
    return connection


def execute_read_query(connection, query):
    try:
        if connection['result'] == 'ERROR':
            print('Прерывание excute_read_query')
            return json.loads('{"Result":"ERROR", "DESC":"Ошибка подключения к серверу"}')
    except:
        print('All_cool')
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"The error '{e}' occurred")
        return "NULL"


def take_db_data(code):
    try:
        connection = create_connection('profiledb', 'sb_pass', 'QNLPGMWWhh2q', '192.168.35.197')
        code = code
        db_req = f"SELECT id FROM public.requests where now() between active_from and active_to and invite_code = {code}"
        resp = execute_read_query(connection, db_req)[0][0]
    except Exception as e :
        return json.loads('{"Result":"ERROR", "DESC":"Глобальная ошибка вычленения данных из базы данных"}')
    return json.loads('{"Result":"SUCCES", "DESC":"'+str(resp)+'"}')


# print(take_db_data('528776'))