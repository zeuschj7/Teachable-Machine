
import cv2
import numpy as np
from keras.models import load_model

import time
import commonutil

# Load the model
model = load_model(commonutil.getRootPath() +'/asset/model/keras_model.h5')

# CAMERA can be 0 or 1 based on default camera of your computer.
camera = cv2.VideoCapture(0)

# Grab the labels from the labels.txt file. This will be used later.
labels = open(commonutil.getRootPath() +'/asset/model/labels.txt', 'r', encoding='utf_8').readlines()

name = 'Not Defined'

while True:
    # Grab the webcameras image.
    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels.
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    cv2.putText(image, name, (0,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0))

    # Show the image in a window
    cv2.imshow('Webcam Image', image)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1
    # Have the model predict what the current image is. Model.predict
    # returns an array of percentages. Example:[0.2,0.8] meaning its 20% sure
    # it is the first label and 80% sure its the second label.
    probabilities = model.predict(image)

    # Print what the highest value probabilitie label
    maxLabel = labels[np.argmax(probabilities)].replace('\n', '').split(' ')

    resultDict = {'maxPb':round(np.max(probabilities) * 100, 2), 'maxId':maxLabel[0], 'maxName':maxLabel[1]}

    print('주어진 모델 중 가장 높은 확률인 {0} % 확률로 {1} 으/로 추정'.format(resultDict['maxPb'], resultDict['maxName']))

    name = str(resultDict['maxId']) +' '+ str(resultDict['maxPb']) +' %'

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)
    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

    # 0.2 sec wait
    time.sleep(0.2)

camera.release()
cv2.destroyAllWindows()
