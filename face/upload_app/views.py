from .modules.face_validation import isFace_in_img
from .modules.face_validation import img_Base64
import requests as RQ
from django.shortcuts import render
from .modules.db import take_db_data


def auth(request):
    valid = False

    #-----------------GET-------------------------
    if request.method == 'GET':

        # берем код для входа
        face_token_ch = request.GET.get('password', False)
        
        # если отправился
        if face_token_ch:

            try:
                data_from_db = take_db_data(face_token_ch)
                print(data_from_db)

            except Exception as e:
                return render(request, './upload_app/auth.html',
                              {'prov': f'Сервер недоступен', "valid": valid})

            if data_from_db['Result'] == 'SUCCES':
                valid = True

            if valid:
                Id = data_from_db['id']
                name = data_from_db['name']

                return render(request, './upload_app/auth.html',
                              {'name': f'{name}', "valid": 'True', "id": f'{Id}', "password":f'{face_token_ch}'})
            else:
                return render(request, './upload_app/auth.html', {"valid": valid})


    #---------------------POST----------------------------
    if request.method == 'POST':
        face_token_ch = request.POST.get('password')
        ID = request.POST['id']
        name = request.POST.get('name')
        file = request.FILES['file_img']
        data_from_db = take_db_data(face_token_ch)
        img, confidence = isFace_in_img(file)

        if data_from_db['Result'] != 'SUCCES':
            print(data_from_db)
            return render(request, './upload_app/auth.html', {'header': 'ОШИБКА'})

        if confidence:

            try:
                img64 = img_Base64(img)

                try:
                    responseVov = RQ.post('http://192.168.48.114:8080/docreateguest', data={
                        "ID": ID,
                        "img64": img64,
                        "name": name

                    })
                    print(name)
                    return render(request, './upload_app/auth.html',
                                  {'header': str(responseVov.json()) + " img: " + str(name)})

                except Exception as e:
                    return render(request, './upload_app/auth.html',
                                  {'no_face': 'Ошибка на сервере Вовы', "valid": "0", "id": f'{ID}'})

            except Exception as e:
                return render(request, './upload_app/auth.html',
                              {'no_face': 'Ошибка кодирования в Base64', "valid": "0", "id": f'{ID}'})

        return render(request, './upload_app/auth.html',
                      {"name":f"{name}", "valid": "0", "id": f'{ID}',
                       "no_face": "На фото не было найдено лицо"})

    return render(request, './upload_app/auth.html', {'header': 'Введите код приглашения'})






def index(request):
    return render(request, './upload_app/auth.html', {'prov': f'Null', "valid": "0"})

