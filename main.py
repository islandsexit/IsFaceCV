import cv2
import numpy as np
import os


prototxt_path = 'mod/deploy.txt'
model_path = "mod/res10_300x300_ssd_iter_140000_fp16.caffemodel"


# загрузим модель Caffe
model = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
img = cv2.imread("./img/under.jpg")



def trust(img_path, not_face=True):
    img = cv2.imread(f"./img/{img_path}")
    for flip in [0, 1, -1]:
        if not not_face:
            img = cv2.flip(img, flip)

        # предварительная обработка: изменение размера и вычитание среднего
        blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), (104.0, 177.0, 123.0))

        # устанавливаем на вход нейронной сети изображение
        model.setInput(blob)

        # выполняем логический вывод и получаем результат
        output = np.squeeze(model.forward())
        for i in range(0, output.shape[0]):
            # получаем уверенность
            confidence = output[i, 2]
            if confidence > 0.80:
                cv2.imwrite(f'./img/1resize_{img_path}', cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR))
                return f"{confidence * 100:.2f}%"
        if flip ==-1:
            return 'No face'


for i in os.listdir('./img'):
    print(f'-------------{i}-------------')
    print(trust(i, False))
    img = cv2.imread(f"./img/{i}")
    print(img.shape)



