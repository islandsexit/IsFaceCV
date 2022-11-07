# Get an instance of a logger

import datetime
import pymysql.cursors
import pymysql
import logging
import requests as RQ
# Get an instance of a logger
logger = logging.getLogger(__name__)





def active_code(code):
    try:
        responseVov = RQ.get(f'http://192.168.15.10:81/getguestbyic?ic={code}')
        responseServ = responseVov.json()
        print(responseVov.json())

        if responseServ['RESULT'] == "SUCCESS":
            name = responseServ['Data']['name'] 
            id = responseServ['Data']['id']
            active = True
            print(name, id)
            return active, id, name
        else:
            return False, "0", "0"
    except Exception as ex:
        print(ex)
        logger.error(str(datetime.datetime.now())+ ";[ERROR];" + "Cannot connect to baseHelper")
        return False, "0", "0"


