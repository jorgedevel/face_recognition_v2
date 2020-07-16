from cv2 import cv2
import time
import sys
import uuid
import os
import MySQLdb as mysql

# connect to database
database = mysql.connect(
    host='localhost',
    user='root',
    password='demo',
    database='recognition'
)
cur = database.cursor()

name_student = sys.argv[1]
lastname_student = sys.argv[2]

cur.execute(f"select id from student where name = '{name_student}' and lastname = '{lastname_student}'")

if len(cur.fetchall()) == 0:
    cur.execute(f"insert into student (name, lastname) values ('{name_student}', '{lastname_student}')")
    database.commit()

WINDOW_NAME = '.:. Register .:.'
DIRNAME_STUDENT = f'resources/{lastname_student} {name_student}'
os.makedirs(DIRNAME_STUDENT, exist_ok=True)

casc_path = os.path.dirname(cv2.__file__) + '/data/haarcascade_frontalface_default.xml' # get path cascade from opencv
face_cascade = cv2.CascadeClassifier(casc_path)

camera = cv2.VideoCapture(0)
camera.set(3, 640)
camera.set(4, 480)

if not camera.isOpened():
    print('[ERROR] on start camera')
    sys.exit()

while True:
    k = cv2.waitKey(125)
    success, frame = camera.read()

    if not success:
        print('[ERROR] on read camera')
        break

    cv2.imshow(WINDOW_NAME, frame)

    if k == 27: # on [Esc]
        print('[EXIT]')
        break

    if k == 13: # on [Enter]
        prev = time.time()
        timer = int(10)

        while timer >= 0:
            success, frame = camera.read()

            if not success:
                print('[ERROR] on read camera')
                break

            cv2.putText(frame, str(timer), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4, cv2.LINE_AA)
            cv2.imshow(WINDOW_NAME, frame)
            cv2.waitKey(125)
            cur = time.time()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(200, 200),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)

            if cur - prev >= 1 & len(faces) == 1:
                prev = cur
                timer-=1
        else:
            success, frame = camera.read()

            if not success:
                print('[ERROR] on read camera')
                break

            cv2.imshow(WINDOW_NAME, frame)
            cv2.waitKey(2000)
            cv2.imwrite(f'{DIRNAME_STUDENT}/{uuid.uuid4()}.jpg', frame)
            print('[CAPTURED]')
camera.release()
cv2.destroyAllWindows()
