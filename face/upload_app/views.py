from logging import raiseExceptions
from random import random

from .modules.face_validation import isFace_in_img
from .modules.face_validation import img_Base64
import requests as RQ
from django.shortcuts import render
from .modules.db import active_code
from django.http import JsonResponse
from django.shortcuts import HttpResponse


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
            active, person, name = active_code(face_token_ch)
            if False:  # active != True:
                raise Exception('Не активный код')

        except Exception as e:
            print(e)
            return render(request, './upload_app/auth.html', {'header': 'ОШИБКА'})

        img, confidence = isFace_in_img(file)
        if confidence:

            try:
                img64 = img_Base64(img)
               # print(img64)

                try:
                    #print('отправляю запрос')
                    responseVov = RQ.post('http://192.168.48.114:8080/docreateguest', data={
                        "ID": person.id,
                        "img64": img64,
                        "name": name

                    })
                    responseServ = responseVov.json()
                    result = responseServ['RESULT']
                    msg = responseServ['DESC']

                    # тут ошибка т.к при хорошем завершении у меня ничего не берется из респонса
                    return JsonResponse({'result': f'{result}', 'msg': f'Попробуйте другое фото.\n Или обратитесть к администратору'})
                    # return render(request, './upload_app/auth.html',
                    #               {'header': str(responseVov.json()) + " img: " + str(name)})

                except:
                    # return render(request, './upload_app/auth.html',
                    #               {'no_face': 'Ошибка на сервере Вовы', "valid": "0", "id": f'{person.id}'})
                    return JsonResponse({'result': f'ERROR', 'msg': f'Ошибка на сервере Вовы'})

            except:

                # return render(request, './upload_app/auth.html',
                #               {'no_face': 'Ошибка кодирования в Base64', "valid": "0", "id": f'{person.id}'})
                return JsonResponse({'result': f'ERROR', 'msg': f'Ошибка кодирования Base64'})

        # return render(request, './upload_app/auth.html',
        #               {"name": f"{name}", "valid": "0", "id": f'{person.id}',
        #                "no_face": "На фото не было найдено лицо"})
        return JsonResponse({'result': f'ERROR', 'msg': f'На фото не было найдено лицо'})

        return JsonResponse({'message': f'{request.POST, request.FILES}'})

    # -----------------GET-------------------------
    if request.method == 'GET':

        # берем код для входа
        face_token_ch = request.GET.get('invite_code', False)
        # print('face_code',face_token_ch)
        # print(request.GET)
        # если отправился
        if face_token_ch and len(face_token_ch) == 6:
            # print('a')
            try:
                active, person, name = active_code(face_token_ch)
                if True:  # active:
                    return render(request, './upload_app/auth.html', {'name': f'{name}', "valid": 'True', "id": f'{person.id}', "password": f'{face_token_ch}'})
                else:
                    return render(request, './upload_app/code.html', {'value_pass': '007'})

            except:

                return render(request, './upload_app/code.html',
                              {'value_pass': '007'})

        else:
            return render(request, './upload_app/code.html', {'value_pass': ''})


def index(request):
    if request.method == 'GET':
        if request.GET.get('master_password', False) == 'secretmasterpasswordvig':
            face_token_ch = request.GET.get('invite_code', False)
            if face_token_ch and len(face_token_ch) == 6:
                # print('a')
                try:
                    active, person, name = active_code(face_token_ch)
                    if True:  # active:
                        return JsonResponse({'RESULT': 'SUCCESS', 'code': f'{person.id}'})
                    else:
                        return JsonResponse({'RESULT': 'ERROR', 'CODE': f'0'})
                except Exception as e:

                    return JsonResponse({'RESULT': 'ERROR', 'CODE': f'{e}'})
        else:
            return JsonResponse({'RESULT': 'AXAXAXAXAXAXAXXAX', 'CODE': 'Im not vindictive. I will write it down.'})
    return JsonResponse({'RESULT': 'ERROR', 'CODE': f'0'})
