from cv2 import cv2
import numpy as np
import face_recognition
import os
import sys
import MySQLdb as mysql

# connect to database
database = mysql.connect(
    host='localhost',
    user='root',
    password='demo',
    database='recognition'
)
cur = database.cursor()

NAME_USER = sys.argv[1]
LAST_NAME_USER = sys.argv[2]

NAME = f'{LAST_NAME_USER} {NAME_USER}'
PATH = f'resources/{NAME}'
IMAGES = []
LIST = os.listdir(PATH)
#print(LIST)

casc_path = os.path.dirname(cv2.__file__) + '/data/haarcascade_frontalface_default.xml' # get path cascade from opencv
face_cascade = cv2.CascadeClassifier(casc_path)
detected_count = 0

for _file in LIST:
    curImg = cv2.imread(f'{PATH}/{_file}')
    IMAGES.append(curImg)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnow = findEncodings(IMAGES)
#print('Succesfully')

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

if cap.isOpened():
    while True:
        success, img = cap.read()

        k = cv2.waitKey(125)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(200, 200),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if len(faces) > 0:
            imgS = cv2.resize(img,(0,0),None,0.25,0.25)
            imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            faceCutFrame = face_recognition.face_locations(imgS)
            encodeCutFrame = face_recognition.face_encodings(imgS, faceCutFrame)

            for encodeFace, faceLoc in zip(encodeCutFrame, faceCutFrame):
                matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)
                #print(faceDis)
                matchIndex = np.argmin(faceDis) #valor minimo

                if matches[matchIndex]:
                    detected_count+=1
                    if detected_count == 20:
                        print(True)
                    y1,x2,y2,x1 = faceLoc
                    #cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                    #cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                    cv2.putText(img,NAME,(x1+6, y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)

        cv2.imshow('Reconocimiento Facial', img)
        
        if k == 27: # on [ESC]
            print('[FINISH]')
            break
    cap.release()
    cv2.destroyAllWindows()
else:
    print('[CAMERA ERROR]')

