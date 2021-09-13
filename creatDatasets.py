import cv2, sys, os
import numpy as np
from queue import Queue
import _thread
from yolov3 import YOLOv3
#haar_file = 'haarcascade_frontalface_default.xml'
datasets = 'datasets'  #All the faces data will be present this folder
sub_data = 'Pooh'     #This will creater folders in datasets with the face of people, so change it's name everytime for the new person.

path = os.path.join(datasets, sub_data)    
if not os.path.isdir(path): 
    os.mkdir(path)
(Width, Height) = (130, 200)    # defining the size of images 


#face_cascade = cv2.CascadeClassifier(haar_file)
webcam = cv2.VideoCapture(1) #'0' is use for my webcam, if you've any other camera attached use '1' like this
yolo = YOLOv3('coco.names','yolov3-tiny.cfg','yolov3-tiny.weights')

# The program loops until it has 30 images of the face.
count = 1
while count <= 250:
    (_, im) = webcam.read()
    faces = yolo.detect(im)
    for d in faces:
        label, left, top, width, height = d
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    #faces = face_cascade.detectMultiScale(gray, 1.3, 4)
        cv2.rectangle(im,(left,top),(left+width,top+height),(255,0,0),2)
        face_crop = gray[top:top + height, left:left + width] 
        if height > 0 and width>0 and top >0 and left >0:
            face_resize = cv2.resize(face_crop, (Width, Height))
        cv2.imwrite('%s/%s.png' % (path,count), face_resize)
    count += 1
    
    cv2.imshow('OpenCV', im)
    key = cv2.waitKey(150)
    if key == 27:
        break
