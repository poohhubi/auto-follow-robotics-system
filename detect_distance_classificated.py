import socket
UDP_IP = "192.168.1.41"
UDP_PORT = 5005

import cv2, sys, numpy, os
from yolov3 import YOLOv3
datasets = 'datasets'
frame_num = 1
real_Height = int(input('ความสูงในหน่วยcm'))
print('Training...')
(images, labels, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            label = id
            images.append(cv2.imread(path, 0))
            labels.append(int(label))
        id += 1
(Width, Height) = (130, 200)

(images, labels) = [numpy.array(lis) for lis in [images, labels]]

yolo = YOLOv3('coco.names','yolov3-tiny.cfg','yolov3-tiny.weights')
model = cv2.face.LBPHFaceRecognizer_create() 
model.train(images,labels)
webcam = cv2.VideoCapture(1)

if not webcam.isOpened():
    raise Exception("Could not open video device")

nub=0
top_set=[]
while True:
    (_, im) = webcam.read()
    body = yolo.detect(im)
    cv2.line(im,(320,0),(320,500),(200,200,0),2)
    cv2.rectangle(im,(240,0),(400,500),(200,200,0),2)
    for d in body:
        label, left, top, width, height = d
        if "person" in str(label):
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            body_crop = gray[top:top + height, left:left + width] 
            if height > 0 and width>0 and top >0 and left >0:
                body_resize = cv2.resize(body_crop, (Width, Height))
                prediction = model.predict(body_resize)
                cv2.rectangle(im,(left,top),(left+width,top+height),(0,255,0),3)
                center = width/2+left
                print(top)
                top_set.append(top)
                nub=nub+1
                if nub == frame_num:
                    print(top_set)
                    sumtop=sum(top_set)
                    AVG=sumtop/frame_num
                    print('AVG',AVG)
                    distance = (AVG* 9.029+1394.5)*real_Height/170
                    print("distance = ",distance)
                    nub=0
                    top_set=[]

                    if distance > 2500:
                        L = 50
                        R = 50
                        if center<240:
                            R-=(center-320)/16
                        elif center>400:
                            L+=(center-320)/16
                    elif distance <2000:
                        L=-50
                        R=-50
                        if center<240:
                            R+=(center-320)*20/640
                        elif center>400:
                            L-=(center-320)*20/640
                    else:
                        L=0
                        R=0
                        if center<240:
                            R-=(center-320)*40/640
                        elif center>400:
                            
                            L+=(center-320)*40/640
                        else:
                            L=0
                            R=0

                    speed = str(str(int(R))+"/"+str(int(L)))
                    MESSAGE = bytes(speed,encoding='utf8')
                    
                    if prediction[1]<100:
                        cv2.putText(im,'%s - %.0f' % (names[prediction[0]],prediction[1]),(left-10, top-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
                        if '%s' % (names[prediction[0]]) == 'Pooh':
                            sock = socket.socket(socket.AF_INET, # Internet
                                            socket.SOCK_DGRAM) # UDP
                            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
                    else:
                        cv2.putText(im,'Unknown',(left-10, top-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))

    cv2.imshow('OpenCV', im)
    if(cv2.waitKey(1) & 0xFF== ord('q')):
        break
webcam.release()
cv2.destroyAllWindows()
