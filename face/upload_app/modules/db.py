from ..models import Requests
from datetime import datetime

def active_code(code):
    date_now = datetime.now().date()
    person  = Requests.objects.get(invite_code = code)
    date_start =person.active_from
    date_stop = person.active_to
    active = date_start<date_now<date_stop
    name = str(person.last_name) + ' ' + str(person.name) + ' ' +  str(person.middle_name)
    return active, person, name