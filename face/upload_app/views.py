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
                print("AJAX| inactive password in POST img64")
                return JsonResponse({'result': f'ERROR', 'msg': f'Заявка неактивна'})

        except Exception as e:
            print("AJAX| exception in POST img64 ",e)
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
                    print(responseServ)
                    # тут ошибка т.к при хорошем завершении у меня ничего не берется из респонса
                    return JsonResponse({'result': f'{result}', 'msg': f'Ошибка. Обратитесть к администратору'})
                    # return render(request, './upload_app/auth.html',
                    #               {'header': str(responseVov.json()) + " img: " + str(name)})

                except:
                    # return render(request, './upload_app/auth.html',
                    #               {'no_face': 'Ошибка на сервере Вовы', "valid": "0", "id": f'{person.id}'})
                    print("error in server registering face")
                    return JsonResponse({'result': f'ERROR', 'msg': f'Ошибка на сервере'})

            except:

                # return render(request, './upload_app/auth.html',
                #               {'no_face': 'Ошибка кодирования в Base64', "valid": "0", "id": f'{person.id}'})
                print("Exception in converting img to base64")
                return JsonResponse({'result': f'ERROR', 'msg': f'Ошибка кодирования Base64'})

        # return render(request, './upload_app/auth.html',
        #               {"name": f"{name}", "valid": "0", "id": f'{person.id}',
        #                "no_face": "На фото не было найдено лицо"})
        print('No Face found')
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
                    print("inactive code")
                    return render(request, './upload_app/code.html', {'value_pass': '007'})

            except:
                print("exception in getting db data")
                return render(request, './upload_app/code.html',
                              {'value_pass': '007'})

        else:
            print("exception in len password")
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
                        return JsonResponse({'RESULT': 'SUCCESS', 'code': f'{person.id}', 'name':f'{name}'})
                    else:
                        print("API|   inactive person")
                        return JsonResponse({'RESULT': 'ERROR', 'CODE': f'Код устарел', 'name':f'0'})
                except Exception as e:
                    print("API|   Exception in database ")
                    return JsonResponse({'RESULT': 'ERROR', 'CODE': f'{e}', 'name':f'{0}'})
        else:
            print("API|   Exception in secretpassword")
            return JsonResponse({'RESULT': 'AXAXAXAXAXAXAXXAX', 'CODE': 'Im not vindictive. I will write it down.', 'name':f'Your_MOTHER'})
    print("API| exception in request type")
    return JsonResponse({'RESULT': 'ERROR', 'CODE': f'0', 'name':f'0'})
