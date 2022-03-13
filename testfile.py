import uuid

import cv2
import numpy as np
import os

from PIL import Image


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



face = r'./mod/front.xml'
eye = r'./mod/eye.xml'
mouth = r'./mod/mouth.xml'
face_cascade_db = cv2.CascadeClassifier(face)
eye_cascade = cv2.CascadeClassifier(eye)
mouth_cascade = cv2.CascadeClassifier(mouth)


def isFace_in_img(imgMem):
    try:
        # img = cv2.imdecode(np.fromstring(imgMem.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        img = cv2.imread('img/leftpos.jpg')
        img = resizing(img, new_width = None,new_height=450)
    except Exception as e:
        print('Проблема с изображением в функции isFace')
    for flip in range(1,10,1):
        img = fix_orientation(img, flip)
        if flip!=-2:
            img = cv2.flip(img, flip)
        print(flip)
        if face_cascade_db.detectMultiScale(img, 1.1, 19)!=():
            print('face')
            eyes = eye_cascade.detectMultiScale(img, 1.1, 19)
            if  eyes !=():
                print('eyes=======',eyes)
                mouths = mouth_cascade.detectMultiScale(img, 1.1, 19)
                print('mouth=======', mouths)
            if mouths !=():
                for (mx, my, mw,mh) in mouths:
                # count=0
                    for (ex, ey, ew, eh) in eyes:
                        if my>ey:
                        # if ey>130 and ey < 320:
                        #     count = count+1
                        #     print(count)
                        #     if count ==2:
                        #         print('all-Cool')
                                return img
    print(12)
    return 12


def fix_orientation(image, orientation):
    # 1 = Horizontal(normal)
    # 2 = Mirror horizontal
    # 3 = Rotate 180
    # 4 = Mirror vertical
    # 5 = Mirror horizontal and rotate 270 CW
    # 6 = Rotate 90 CW
    # 7 = Mirror horizontal and rotate 90 CW
    # 8 = Rotate 270 CW

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


name_img = str(uuid.uuid4()) + '.png'
cv2.imwrite(name_img, isFace_in_img('dddd'))
print(name_img)
image = Image.open(name_img)
image.show()