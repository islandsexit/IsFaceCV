import requests as RQ
from django.shortcuts import render
from .forms import FaceFormRegister


# from face.upload_app.take_db_response import take_db_data


def auth(request):
    if request.method == 'GET':
        face_token_ch = request.GET.get('password', False)
        if face_token_ch:
            try:
                data_from_db = take_db_data(face_token_ch)
            except Exception as e:
                return render(request, 'auth.html',
                              {'prov': 'Сервер недоступен', "valid": '0'})

            valid = True if data_from_db['Result'] == 'SUCCES' else False
            if valid:
                Id = data_from_db['DESC']
                return render(request, 'auth.html', {'prov': 'Ваш код работает исправно', "valid": valid, "id":f'{Id}'})
            else: return render(request, 'auth.html', {'prov': 'Такого кода не существует', "valid": valid})



    if request.method == 'POST':

        ID = request.POST['id']
        file = request.FILES['file_img']
        confidence = isFace_in_img(file)
        if confidence > 90:
            try:
                img64 = img_Base64(file)
                try:
                    responseVov = RQ.post('http://192.168.48.114:8080/docreateguest', data={
                            "ID": ID,
                            "img64": img64
                        })
                    print(responseVov)
                except Exception as e:
                    return render(request, 'auth.html', {'prov': 'Ошибка на сервере Вовы', "valid": "0", "id": f'{ID}'})
            except Exception as e:
                return render(request, 'auth.html', {'prov': 'Ошибка кодирования в Base64', "valid": "0", "id":f'{ID}'})

            return render(request, 'auth.html', {'prov': 'Отправил запрос к вове', "succes":True})
        return render(request, 'auth.html', {'prov': f'Не удалось найти лицо, пожалуйста отправьте другое фото', "valid": "0", "id":f'{ID}'})

    return render(request, 'auth.html', {'prov': 'Blyt2'})


def index(request):
    return render(request, 'index.html', {'prov': 'Oshibka', 'form': FaceFormRegister()})



#----------------------Временное решение с Base64-----------------
import base64

def img_Base64(imgMem):
    try:
        return base64.b64encode(imgMem.read())
    except Exception as e:
        return None



#---------------------Конец временного решения с Base64-----------------



#-------------------------Временное решение с opencv---------------
import cv2
import numpy as np
import os

prototxt_path = '../mod/deploy.txt'
model_path = "../mod/res10_300x300_ssd_iter_140000_fp16.caffemodel"
model = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

def isFace_in_img(imgMem):
    try:
        img = cv2.imdecode(np.fromstring(imgMem.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        print('IMG zagryzilos')
        blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), (104.0, 177.0, 123.0))

        # устанавливаем на вход нейронной сети изображение
        model.setInput(blob)

        # выполняем логический вывод и получаем результат
        output = np.squeeze(model.forward())
        for i in range(0, output.shape[0]):
            # получаем уверенность
            confidence = output[i, 2]
            if confidence > 0.80:
                return confidence * 100
    except Exception as e:
        print('Zalupa')
        return 0
    return 0

#------------------------Конец временного решения с OPenCV---------------------------








# ----------------------------Временное решение c базой данных----------------------
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
    except Exception as e:
        return json.loads('{"Result":"ERROR", "DESC":"Глобальная ошибка вычленения данных из базы данных"}')
    return json.loads('{"Result":"SUCCES", "DESC":"' + str(resp) + '"}')


# ----------------------------Конец временного решения--------------


def index(request):
    return render(request, 'index.html', {'prov': 'Oshibka', 'form': FaceFormRegister()})
#     face = Face.objects.all()
#
#     if request.method == 'GET':
#         try:
#             data = {
#                 'face_id_ch': request.GET['face_id_ch'],
#                 'face_name_ch': request.GET['face_name_ch']
#             }
#         except :
#             data = {}
#         return render(request, 'index.html', {'prov': request, 'face': face, 'form': FaceFormRegister(data)})
#
#     if request.method == 'POST':
#         try:
#             print(request.FILES)
#             form = FaceFormRegister(request.POST, request.FILES)
#             if form.is_valid():
#                 face_id = form.cleaned_data.get('face_id_ch')
#                 name = form.cleaned_data.get("face_name_ch")
#                 img = form.cleaned_data.get("face_img")
#                 token = form.cleaned_data.get('face_token_int')
#                 token_valid = 'True'
#                 group = form.cleaned_data.get('face_group_ch')
#                 worker = form.cleaned_data.get('face_worker_bol')
#                 obj = Face.objects.create(
#                     face_id_ch=face_id,
#                     face_name_ch=name,
#                     face_img=img,
#                     face_token_int=token,
#                     face_token_valid_bol=token_valid,
#                     face_group_ch=group,
#                     face_worker_bol=worker
#                 )
#                 obj.save()
#                 print(obj)
#                 return  render(request, 'index.html', {'prov': 'Yeeees', 'face': face,'form':FaceFormRegister()})
#         except Exception as e:
#             render(request, 'index.html', {'prov': 'Oshibka', 'face': face, 'form': FaceFormRegister()})
#
#
#     return render(request, 'index.html', {'prov': 'request', 'face': face,'form':FaceFormRegister()})


# def added(request):
#     # if request.method == "POST" and request.POST:
#     # try:
#     #         face_id = request.POST['face_id']
#     #        print('ok')
#     #       face_name = request.POST['face_name']
#     #      print('ok')
#     #     face_img = request.FILES['face_img']
#     #    print('ok')
#     #   created_obj = Face.objects.create(face_id=face_id, face_name=face_name, face_img=face_img)
#     #  print('ok')
#     # created_obj.save()
#     # except Exception as e:
#     #   return HttpResponse(e)
#
#     # context = {}
#     # if request.method == "POST":
#     #     form = FaceForm(request.POST)
#     #     # if form.is_valid():
#     #     print('form is valid')
#     #     face_name = request.POST.get("face_name")
#     #     face_img = request.POST.get("face_id")
#     #     face_id = request.FILES['face_img']
#     #     created_obj = Face.objects.create(face_id=face_id, face_name=face_name, face_img=face_img)
#     #     print('ok')
#     #     created_obj.save()
#     #     print(created_obj)
#     #     # else:
#     #     # form = FaceForm()
#     #     context['form'] = form
#
#     if request.method == 'POST':
#         print(request.FILES)
#         form = FaceForm(request.POST, request.FILES)
#         if form.is_valid():
#             face_id = form.cleaned_data.get('face_id')
#             name = form.cleaned_data.get("face_name")
#             img = form.cleaned_data.get("face_img")
#             obj = Face.objects.create(
#                 face_id=face_id,
#                 face_img=img,
#                 face_name=name
#             )
#             obj.save()
#             print(obj)
#             return HttpResponse('OK')
#
#
#     #return HttpResponse('mmmmmm')
