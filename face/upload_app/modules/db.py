
import requests as RQ
# Get an instance of a logger
import logging
logger = logging.getLogger(__name__)
import datetime


def active_code(code):
    try:
        response_code = RQ.post('http://192.168.48.132:1237/FindGuest', data={
                        "INVITECODE": code,

                    })
        if response_code.status_code == 200:
           response_code = response_code.json()
           id = response_code["DATA"][0]["FID"]
           name = response_code["DATA"][0]["Name"]
           active = True 
        else:
            return False, "0", "0"
    except Exception as e:
        logger.error(str(datetime.datetime.now())+ ";[ERROR];" + f"code = {code} cannot connect to db server")
        return False, "0", "0"
    return active, id, name