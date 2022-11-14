import datetime
from logging import raiseExceptions
from random import random
from django.http import HttpResponseNotFound
from django.template import loader

from .modules.face_validation import isFace_in_img
from .modules.face_validation import img_Base64
import requests as RQ
from django.shortcuts import render
from .modules.db import active_code
from django.http import JsonResponse
from django.shortcuts import HttpResponse
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


STAFF_ALREADY_EXIST = "LAN_EXP-3005"
PHOTO_ALREADY = "LAN_EXP-4043"
ABNORMAL_IMAGE = "LAN_EXP-4011"
MULTIPLE_FACES = "LAN_EXP-8007"
FACE_TOO_SMALL = "LAN_EXP-8010"
FACE_TOO_LARGE_OR_INCOMPLETE = "LAN_EXP-8013"
FACE_ANGEL_TOO_LARGE = "LAN_EXP-8014"
FACE_TOO_DARK_OR_TOO_LIGHT = "LAN_EXP-8015"
FACE_MOVES = "LAN_EXP-8016"
FACE_TOO_DARK = "LAN_EXP-8017"

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def auth(request):
    valid = False

    if is_ajax(request):
        face_token_ch = request.POST.get('invite_code')
        ID = request.POST['id']
        name = request.POST.get('name')
        file = request.FILES['upload_file']
        try:
            active, id, name = active_code(face_token_ch)
            if active != True:
                logger.error(str(datetime.datetime.now()) +
                             ";[ERROR];"+f"AJAX| code ={face_token_ch}inactive password in POST img64")
                return JsonResponse({'result': f'ERROR', 'msg': f'Заявка неактивна'})

        except Exception as e:

            logger.error(str(datetime.datetime.now()) +
                         ";[ERROR];"+f"AJAX| code ={face_token_ch} exception in POST img64 ", e)
            return render(request, './upload_app/auth.html', {'header': 'ОШИБКА'})

        img, confidence = isFace_in_img(file)
        if confidence:

            try:
                img64 = img_Base64(img)
               # logger.error(str(datetime.datetime.now())+ " " + img64)

                try:
                    #logger.error(str(datetime.datetime.now())+ " " + 'отправляю запрос')
                    responseVov = RQ.post('http://192.168.15.10:1235/addPersonWithFace', data={
                        "id": id,
                        "img64": img64,
                        "name": name,
                        "isGuest":1

                    })
                    responseServ = responseVov.json()
                    print(responseServ)
                    result = responseServ['RESULT']
                    msg = 'Ошибка. Попробуйте еще раз.'
                    if result == "ERROR":
                        code_error = responseServ['DATA']['code']
                        if  code_error == STAFF_ALREADY_EXIST:
                            msg = "Ошибка. Код был уже использован."
                        elif code_error == PHOTO_ALREADY:
                            msg = "Ошибка. Ваше лицо уже зарегистрировано в системе."
                        elif code_error == ABNORMAL_IMAGE:
                            msg = "Ошибка. Проблема с файлом."
                        elif code_error == MULTIPLE_FACES:
                            msg = "Ошибка. На фото было замечено несколько лиц."
                        elif code_error == FACE_TOO_SMALL:
                            msg = "Ошибка. Лицо слишком далеко."
                        elif code_error == FACE_TOO_LARGE_OR_INCOMPLETE:
                            msg = "Ошибка. Лицо слишком близко."
                        elif code_error == FACE_ANGEL_TOO_LARGE:
                            msg = "Ошибка. Лицо было снято под углом"
                        elif code_error == FACE_TOO_DARK_OR_TOO_LIGHT:
                            msg = "Ошибка. Плохое освещение"
                        elif code_error == FACE_MOVES:
                            msg = "Ошибка. Лицо было снято в движении"
                        elif code_error == FACE_TOO_DARK:
                            msg = "Ошибка. Фото слишком темное"
                        else:
                            logger.error(str(datetime.datetime.now()) +
                                 ";[ERROR];"+f"{responseServ}")
                    
                    print(responseServ)
                    # тут ошибка т.к при хорошем завершении у меня ничего не берется из респонса
                    return JsonResponse({'result': f'{result}', 'msg': f'{msg}'})

                except Exception as e:
                    print(e)
                    logger.error(str(datetime.datetime.now()) +
                                 ";[ERROR];"+f"code ={face_token_ch} error in server registering face, {e.with_traceback}")
                    return JsonResponse({'result': f'ERROR', 'msg': f'Ошибка на сервере'})

            except:

                # return render(request, './upload_app/auth.html',
                #               {'no_face': 'Ошибка кодирования в Base64', "valid": "0", "id": f'{person.id}'})
                logger.error(str(datetime.datetime.now()) +
                             ";[ERROR];"+f"code ={face_token_ch} Exception in converting img to base64")
                return JsonResponse({'result': f'ERROR', 'msg': f'Ошибка кодирования Base64'})

        # return render(request, './upload_app/auth.html',
        #               {"name": f"{name}", "valid": "0", "id": f'{person.id}',
        #                "no_face": "На фото не было найдено лицо"})
        logger.error(str(datetime.datetime.now()) +
                     ";[ERROR];"+f'code ={face_token_ch} No Face found')
        return JsonResponse({'result': f'ERROR', 'msg': f'На фото не было найдено лицо'})

    # -----------------GET-------------------------
    if request.method == 'GET':
        try:
            face_token_ch = read_code(request.GET['id'])
            print(face_token_ch)

            if face_token_ch and len(face_token_ch) == 6:
                try:
                    active, id, name = active_code(face_token_ch)
                    print(active, id, name)
                    if active:  # active:
                        logger.error(str(datetime.datetime.now()) +
                                    ";[INFO];" + f"SITE| code ={face_token_ch} VISITOR  ")
                        return render(request, './upload_app/auth.html', {'name': f'{name}', "valid": 'True', "id": f'{id}', "password": f'{face_token_ch}'})
                    else:
                        logger.error(str(datetime.datetime.now()) +
                                    ";[ERROR];" + f"code ={face_token_ch} inactive code")
                        return render(request, './upload_app/code.html', {'value_pass': '007'})

                except Exception as ex:
                    print("View Exception", ex)
                    logger.error(str(datetime.datetime.now()) +
                                ";[ERROR];"+f"code ={face_token_ch} exception in getting db data")
                    return render(request, './upload_app/code.html',
                                {'value_pass': '007'})
            else:
                logger.error(str(datetime.datetime.now()) +
                                    ";[ERROR];" + f"code ={face_token_ch} inactive code")
                return render(request, './upload_app/code.html', {'value_pass': '007'})

        except Exception as e:
            logger.error(str(datetime.datetime.now()) +";[INFO];"+"visitor on main template")
            return render(request, './upload_app/code.html', {'value_pass': ''})

    if request.method == 'POST':

        # берем код для входа
        face_token_ch = request.POST.get('invite_code', False)
        # logger.error(str(datetime.datetime.now())+ " " + 'face_code',face_token_ch)
        # logger.error(str(datetime.datetime.now())+ " " + request.GET)
        # если отправилсяx
        if face_token_ch and len(face_token_ch) == 6:
            # logger.error(str(datetime.datetime.now())+ " " + 'a')
            try:
                active, id, name = active_code(face_token_ch)
                print(active, id, name)
                if active:  # active:
                    logger.error(str(datetime.datetime.now()) +
                                 ";[INFO];" + f"SITE| code ={face_token_ch} VISITOR  ")
                    return render(request, './upload_app/auth.html', {'name': f'{name}', "valid": 'True', "id": f'{id}', "password": f'{face_token_ch}'})
                else:
                    logger.error(str(datetime.datetime.now()) +
                                 ";[ERROR];" + f"code ={face_token_ch} inactive code")
                    return render(request, './upload_app/code.html', {'value_pass': '007'})

            except Exception as ex:
                print("View Exception", ex)
                logger.error(str(datetime.datetime.now()) +
                             ";[ERROR];"+f"code ={face_token_ch} exception in getting db data")
                return render(request, './upload_app/code.html',
                              {'value_pass': '007'})
        else:
            logger.error(str(datetime.datetime.now()) +
                                 ";[ERROR];" + f"code ={face_token_ch} inactive code")
            return render(request, './upload_app/code.html', {'value_pass': '007'})


def index(request):
    
    return JsonResponse({'RESULT': 'ERROR', 'code': f'0', 'name': f'0'})


def page_not_found(request, exception):
    content = loader.render_to_string('./upload_app/custom_40x.html', {}, request)
    return HttpResponseNotFound(content)





def read_code(code: str) -> str:
    half_size = int(((len(code) - 1) / 2))
    step = int(code[half_size])

    key = list()

    key.append(code[15 - step])
    key.append(code[15 - step*2])
    key.append(code[15 - step*3])

    key.append(code[15 + step])
    key.append(code[15 + step*2])
    key.append(code[15 + step*3])

    ret_val = ''.join(key)

    return ret_val

