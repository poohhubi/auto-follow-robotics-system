import cv2, sys, numpy, os
from yolov3 import YOLOv3
datasets = 'datasets'
frame_num = 5
real_Height = int(input('ความสูงในหน่วยmm'))
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
webcam = cv2.VideoCapture(2)

if not webcam.isOpened():
    raise Exception("Could not open video device")

nub=0
height_set=[]
while True:
    (_, im) = webcam.read()
    body = yolo.detect(im)
    for d in body:
        label, left, top, width, height = d
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        body_crop = gray[top:top + height, left:left + width] 
        if height > 0 and width>0 and top >0 and left >0:
            body_resize = cv2.resize(body_crop, (Width, Height))

            prediction = model.predict(body_resize)
            cv2.rectangle(im,(left,top),(left+width,top+height),(0,255,0),3)
            print(height)
            height_set.append(height)
            nub=nub+1
            if nub == frame_num:
                print(height_set)
                sumheight=sum(height_set)
                AVG=sumheight/frame_num
                print('AVG',AVG)
                distance = (AVG*(-12.245)+6622.4) * (real_Height / 1720)
                print("distance = ",distance)
                nub=0
                height_set=[]
        
            if prediction[1]<100:
                cv2.putText(im,'%s - %.0f' % (names[prediction[0]],prediction[1]),(left-10, top-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
            else:
                cv2.putText(im,'Unknown',(left-10, top-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))

    cv2.imshow('OpenCV', im)
    if(cv2.waitKey(1) & 0xFF== ord('q')):
        break
webcam.release()
cv2.destroyAllWindows()
