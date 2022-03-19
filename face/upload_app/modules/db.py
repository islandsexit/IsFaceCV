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
        return json.loads('{"Result":"ERROR", "DESC":"Ошибка подключения к серверу"}')
    return connection


def execute_read_query(connection, query):
    try:
        if connection['result'] == 'ERROR':
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
        return "NULL"


def take_db_data(code):
    debag=True
    try:
        connection = create_connection('profiledb', 'sb_pass', 'QNLPGMWWhh2q', '192.168.35.197')
        code = code
        db_req = f"SELECT id, name, last_name, middle_name FROM public.requests where now() between active_from and active_to and invite_code = {code}"
        if debag:
            db_req = f"SELECT id, name, last_name, middle_name FROM public.requests where invite_code = {code}"
        try:
            id = execute_read_query(connection, db_req)[0][0]
            name = execute_read_query(connection, db_req)[0][2] + ' ' + execute_read_query(connection, db_req)[0][
                1] + ' ' + execute_read_query(connection, db_req)[0][3]
        except Exception:
            return json.loads('{"Result":"ERROR", "DESC":"Такого кода не существует"}')
    except Exception as e:
        return json.loads('{"Result":"ERROR", "DESC":"Сервер недоступен, повторите позднее"}')
    return json.loads('{"Result":"SUCCES", "id":"' + str(id) + '", "name":"' + str(name) + '"}')