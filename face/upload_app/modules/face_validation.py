import cv2
import numpy as np
import os
import base64
import uuid

face = r'../mod/front.xml'
eye = r'../mod/eye.xml'
mouth = r'../mod/mouth.xml'
face_cascade_db = cv2.CascadeClassifier(face)
eye_cascade = cv2.CascadeClassifier(eye)
mouth_cascade = cv2.CascadeClassifier(mouth)


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





def isFace_in_img(imgMem):
    try:
        
        img = cv2.imdecode(np.fromstring(imgMem.file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        img = resizing(img, new_width=None, new_height=450)
        
    except Exception as e:
        print(e)
        return 12, False
    try:
        for flip in range(1, 10, 1):
            img = fix_orientation(img, flip)
            faces = face_cascade_db.detectMultiScale(img, 1.1, 19)
           
            if faces != ():
                for (x, y, w, h) in faces:
                    height_face_1_3=int(h/3)
                    height_face_1_6 = int(h / 6)
                    weight_face_1_6=int(w/6)
                    print(len(img), 'img')
                    img_face = img[y-height_face_1_3:y+h+height_face_1_6, x-weight_face_1_6:x+w+weight_face_1_6]
                    print(img_face, 'img_face')
                    if len(img_face) == 0:
                        img_face = img
                        print(img_face, 'new cropped')
                    eyes = eye_cascade.detectMultiScale(img, 1.1, 19)
                    if eyes != ():
                        mouths = mouth_cascade.detectMultiScale(img, 1.1, 19)
                        if mouths != ():
                            for (mx, my, mw, mh) in mouths:
                                count_ey = 0
                                count_my_ey = False
                                for (ex, ey, ew, eh) in eyes:
                                    if True:#ey - my > 60:
                                        count_my_ey = True
                                    if True:  # 140 < ey < 320:
                                        count_ey = count_ey + 1
                                        if count_ey == 2:
                                            if True:  # count_my_ey:
                                                
                                                return img_face, True
    except Exception as e:
        print(e)
        return 12, False
    return 12, False




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




def img_Base64(imgMem):
    try:
        name_img = str('/home/vig/django/IsFaceCV/face/upload_app/temp/') + str(uuid.uuid4()) + '.png'
        #name_img = str(uuid.uuid4()) + '.png'

        cv2.imwrite(name_img, imgMem)

        with open(name_img, "rb") as image_file:

            encoded_string = base64.b64encode(image_file.read())

        os.remove(name_img)
        
        return encoded_string
    except Exception as e:
        print(e)
    return None