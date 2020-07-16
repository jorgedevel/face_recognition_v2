from cv2 import cv2
import time
import os
import uuid
import MySQLdb as mysql
import sys

# connect to database
database = mysql.connect(
    host='localhost',
    user='root',
    password='demo',
    database='recognition'
)
cur = database.cursor()
#print('*'*10 + ' APPLICATION CONNECTED TO DATABASE ' + '*'*10)

ON_REGISTER = '.:. Register .:.'
ON_READY = '.:. Countdowner for capture image .:.'

#print('*'*10 + ' APPLICATION NEED THIS INFORMATION ' + '*'*10)
NAME_USER = sys.argv[1]  #input('1. Your first name: ')
LAST_NAME_USER = sys.argv[2] #input('2. Your last name: ')

cur.execute('INSERT INTO student (name, lastname) VALUES (%s, %s)', (NAME_USER, LAST_NAME_USER))
database.commit() # save changes

DIRNAME_USER = f'resources/{LAST_NAME_USER} {NAME_USER}'
os.makedirs(DIRNAME_USER, exist_ok=True)

casc_path = os.path.dirname(cv2.__file__) + '/data/haarcascade_frontalface_default.xml' # get path cascade from opencv
face_cascade = cv2.CascadeClassifier(casc_path)
#print('*'*10 + ' STARTING WEBCAM ' + '*'*10)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
count = 0

if cap.isOpened():
    while True:
        _, img = cap.read()
        k = cv2.waitKey(125)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, '10', (50, 0), font, 2, (76, 153, 0), 4, cv2.LINE_AA)
        cv2.imshow(ON_REGISTER, img)
        
        if k == 13: # on [Enter]
            #detect_number = 0
            TIMER = int(10)
            cv2.destroyWindow(ON_REGISTER)
            prev = time.time()
            
            while TIMER >= 0:
                _, img = cap.read()
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, str(TIMER), (100, 100), font, 7, (76, 153, 0), 4, cv2.LINE_AA)
                cur = time.time()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=5,
                    minSize=(200, 200),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )

                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)
                if cur - prev >= 1 & len(faces) > 0:
                    #detect_number+=1
                    #print(f'detect: {detect_number}')
                    prev = cur
                    TIMER-=1
                cv2.imshow(ON_READY, img)
            else:
                _, img = cap.read()
                cv2.imwrite(f'{DIRNAME_USER}/{uuid.uuid4()}.jpg', img)
                count+=1
                print(f'[CAPTURED] {count} image(s)')
                cv2.destroyWindow(ON_READY)
        elif k == 27: # on [ESC]
            print('[FINISH]')
            break
    cap.release()
    cv2.destroyAllWindows()
else:
    print('[CAMERA ERROR]')
