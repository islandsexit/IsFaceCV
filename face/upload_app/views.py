import uuid

import requests as RQ
from django.shortcuts import render


def auth(request):
    valid = True
    if request.method == 'GET':
        face_token_ch = request.GET.get('password', False)
        if face_token_ch:
            # try:
            #     data_from_db = take_db_data(face_token_ch)
            #     print(data_from_db)
            # except Exception as e:
            #     return render(request, './upload_app/auth.html',
            #                   {'prov': f'Сервер недоступен', "valid": valid})
            # if data_from_db['Result'] == 'SUCCES':
            #     valid = True

            if valid:
                # Id = data_from_db['DESC']
                return render(request, './upload_app/auth.html',
                      {'prov': 'Ваш код работает исправно', "valid": 'True', "id": f'{31}'})
            # else:
                # return render(request, './upload_app/auth.html', {'header': data_from_db['DESC'], "valid": valid})

    if request.method == 'POST':

        ID = request.POST['id']
        file = request.FILES['file_img']
        img, confidence = isFace_in_img(file)
        if confidence:
            try:
                img64 = img_Base64(img)
                try:
                    responseVov = RQ.post('http://192.168.48.114:8080/docreateguest', data={
                        "ID": ID,
                        "img64": img64
                    })

                    return render(request, './upload_app/auth.html', {'header': str(responseVov.json())+" img: "+str(img64)})
                except Exception as e:
                    return render(request, './upload_app/auth.html', {'prov': 'Ошибка на сервере Вовы', "valid": "0", "id": f'{ID}'})
            except Exception as e:
                return render(request, './upload_app/auth.html',
                              {'prov': 'Ошибка кодирования в Base64', "valid": "0", "id": f'{ID}'})

            return render(request, './upload_app/auth.html', {'prov': 'Отправил запрос к вове', "succes": True})
        return render(request, './upload_app/auth.html',
                      {'prov': f'Не удалось найти лицо, пожалуйста отправьте другое фото', "valid": "0", "id": f'{ID}', "no_face":"На фото не было найдено лицо"})

    return render(request, './upload_app/auth.html', {'header': 'Введите код приглашения'})


def index(request):
    return render(request, './upload_app/auth.html', {'prov': f'Null', "valid": "0"})


# ----------------------Временное решение с Base64-----------------
import base64


def img_Base64(imgMem):
    try:
        name_img = str(uuid.uuid4()) + '.png'
        print(name_img)
        cv2.imwrite(name_img, imgMem)
        print('image written')
        with open(name_img, "rb") as image_file:
            print(image_file)
            encoded_string = base64.b64encode(image_file.read())
        print("image readed")
        os.remove(name_img)
        print("image removed")
        return encoded_string
    except Exception as e:
        print(e)
        return None


# ---------------------Конец временного решения с Base64-----------------


# ----------------------Временное решение Переворота изображения------------
def fix_orientation(image, orientation):

    if type(orientation) is list:
        orientation = orientation[0]

    if orientation == 1:
        pass
    elif orientation == 2:
        image = cv2.flip(image, 0)
    elif orientation == 3:
        image = cv2.rotate(image, cv2.ROTATE_180)
    elif orientation == 4:
        image = cv2.flip(image, 1)
    elif orientation == 5:
        image = cv2.flip(image, 0)
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif orientation == 6:
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif orientation == 7:
        image = cv2.flip(image, 0)
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif orientation == 8:
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif orientation == 9:
        image = cv2.flip(image, -1)

    return image

# ----------------------Конец временного решения Переворота изображения----------

# -------------------------Временное решение с opencv---------------
import cv2
import numpy as np
import os


def resizing(img, new_width=None, new_height=None, interp=cv2.INTER_LINEAR):
    h, w = img.shape[:2]

    if new_width is None and new_height is None:
        return img

    if new_width is None:
        ratio = new_height / h
        dimension = (int(w * ratio), new_height)

    else:
        ratio = new_width / w
        dimension = (new_width, int(h * ratio))

    return cv2.resize(img, dimension, interpolation=interp)


face = r'../mod/front.xml'
eye = r'../mod/eye.xml'
mouth = r'../mod/mouth.xml'
face_cascade_db = cv2.CascadeClassifier(face)
eye_cascade = cv2.CascadeClassifier(eye)
mouth_cascade = cv2.CascadeClassifier(mouth)


def isFace_in_img(imgMem):
    try:
        img = cv2.imdecode(np.fromstring(imgMem.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        img = resizing(img, new_width=None, new_height=450)
    except Exception as e:
        print('error')
    for flip in range(1, 10, 1):
        img = fix_orientation(img, flip)
        if face_cascade_db.detectMultiScale(img, 1.1, 19) != ():
            eyes = eye_cascade.detectMultiScale(img, 1.1, 19)
            if eyes != ():
                mouths = mouth_cascade.detectMultiScale(img, 1.1, 19)
                if mouths != ():
                    for (mx, my, mw, mh) in mouths:
                        count_ey = 0
                        count_my_ey = False
                        for (ex, ey, ew, eh) in eyes:
                            if ey - my > 60:
                                count_my_ey = True
                            if True:#140 < ey < 320:
                                count_ey = count_ey+1
                                if count_ey ==2:
                                    if True :#count_my_ey:
                                        return img, True
    return 12, False




# ------------------------Конец временного решения с OPenCV---------------------------


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
    try:
        connection = create_connection('profiledb', 'sb_pass', 'QNLPGMWWhh2q', '192.168.35.197')
        code = code
        db_req = f"SELECT id FROM public.requests where now() between active_from and active_to and invite_code = {code}"
        try:
            resp = execute_read_query(connection, db_req)[0][0]
        except Exception:
            return json.loads('{"Result":"ERROR", "DESC":"Такого кода не существует"}')
    except Exception as e:
        return json.loads('{"Result":"ERROR", "DESC":"Сервер недоступен, повторите позднее"}')
    return json.loads('{"Result":"SUCCES", "DESC":"' + str(resp) + '"}')


# ----------------------------Конец временного решения--------------


def index(request):
    return render(request, './upload_app/index.html', {'prov': 'Oshibka'})
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
