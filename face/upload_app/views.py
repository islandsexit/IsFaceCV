from logging import raiseExceptions

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
        face_token_ch = request.POST.get('password')
        ID = request.POST['id']
        name = request.POST.get('name')
        file = request.FILES['upload_file']
        try:
            active, person, name = active_code(face_token_ch)
            if False:  # active != True:
                raise Exception('Не активный код')

        except e as Exception:
            print(e)
            return render(request, './upload_app/auth.html', {'header': 'ОШИБКА'})

        img, confidence = isFace_in_img(file)
        if confidence:

            try:
                img64 = img_Base64(img)
                print(img64)

                try:
                    print('отправляю запрос')
                    responseVov = RQ.post('http://192.168.48.114:8080/docreateguest', data={
                        "ID": person.id,
                        "img64": img64,
                        "name": name

                    })
                    responseServ = responseVov.json()
                    result = responseServ['RESULT']
                    msg = responseServ['DESC']
                    
                    return JsonResponse({'result':f'{result}','msg':f'{msg}'})
                    # return render(request, './upload_app/auth.html',
                    #               {'header': str(responseVov.json()) + " img: " + str(name)})
                    

                except :
                    # return render(request, './upload_app/auth.html',
                    #               {'no_face': 'Ошибка на сервере Вовы', "valid": "0", "id": f'{person.id}'})
                    return JsonResponse({'result':f'ERROR','msg':f'Ошибка на сервере Вовы'})

            except:
                
                # return render(request, './upload_app/auth.html',
                #               {'no_face': 'Ошибка кодирования в Base64', "valid": "0", "id": f'{person.id}'})
                return JsonResponse({'result':f'ERROR','msg':f'Ошибка кодирования Base64'})

        # return render(request, './upload_app/auth.html',
        #               {"name": f"{name}", "valid": "0", "id": f'{person.id}',
        #                "no_face": "На фото не было найдено лицо"})
        return JsonResponse({'result':f'ERROR','msg':f'На фото не было найдено лицо'})

        return JsonResponse({'message': f'{request.POST, request.FILES}'})

    # -----------------GET-------------------------
    if request.method == 'GET':

        # берем код для входа
        face_token_ch = request.GET.get('password', False)

        # если отправился
        if face_token_ch and len(face_token_ch) == 6:
            print('a')
            try:
                active, person, name = active_code(face_token_ch)
                if True:  # active:
                    return render(request, './upload_app/auth.html', {'name': f'{name}', "valid": 'True', "id": f'{person.id}', "password": f'{face_token_ch}'})
                else:
                    return render(request, './upload_app/auth.html', {'header': f'Такого кода не существует', "valid": valid})

            except:

                return render(request, './upload_app/auth.html',
                              {'header': f'Такого кода не существует', "valid": valid})

        else:
            return render(request, './upload_app/auth.html', {'header': 'Введите код', "valid": 0})

    # ---------------------POST----------------------------
    if request.method == 'POST':
        face_token_ch = request.POST.get('password')
        ID = request.POST['id']
        name = request.POST.get('name')
        file = request.FILES['file_img']
        print(file)
        try:
            active, person, name = active_code(face_token_ch)
            if False:  # active != True:
                raise Exception('Не активный код')

        except e as Exception:
            print(e)
            return render(request, './upload_app/auth.html', {'header': 'ОШИБКА'})

        img, confidence = isFace_in_img(file)

        if confidence:

            try:

                img64 = img_Base64(img)

                try:
                    responseVov = RQ.post('http://192.168.48.114:8080/docreateguest', data={
                        "ID": person.id,
                        "img64": img64,
                        "name": name

                    })
                    print(name)
                    return render(request, './upload_app/auth.html',
                                  {'header': str(responseVov.json()) + " img: " + str(name)})

                except Exception as e:
                    return render(request, './upload_app/auth.html',
                                  {'no_face': 'Ошибка на сервере Вовы', "valid": "0", "id": f'{person.id}'})

            except Exception as e:
                print(e)
                return render(request, './upload_app/auth.html',
                              {'no_face': 'Ошибка кодирования в Base64', "valid": "0", "id": f'{person.id}'})

        return render(request, './upload_app/auth.html',
                      {"name": f"{name}", "valid": "0", "id": f'{person.id}',
                       "no_face": "На фото не было найдено лицо"})

    return render(request, './upload_app/auth.html', {'header': 'Введите код приглашения'})


def index(request):
    return render(request, './upload_app/auth.html', {'prov': f'Null', "valid": "0"})
