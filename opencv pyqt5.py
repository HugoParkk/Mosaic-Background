import cv2
import pyvirtualcam
import threading
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

running = False
def run():
    xml = 'haarcascade_frontalface_alt2.xml'
    face_cascade = cv2.CascadeClassifier(xml)

    global running
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    fmt = pyvirtualcam.PixelFormat.BGR
    with pyvirtualcam.Camera(width=frame.shape[1], height=frame.shape[0], fps=30, fmt=fmt, print_fps=True) as cam:
        while running:
            ret, frame = cap.read()
            
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray,1.05, 5)
                print("Number of faces detected: " + str(len(faces)))
                
                mask = frame
                mask = cv2.resize(mask, dsize=(0, 0), fx=0.04, fy=0.04) # 축소
                mask = cv2.resize(mask, (640, 480), interpolation=cv2.INTER_AREA) # 확대

                if len(faces):
                    for (x,y,w,h) in faces:
                        cv2.rectangle(frame,(x-50,y-50),(x+w+50,y+h+50),(255,0,0),2)
                        
                        # mask = np.zeros(frame.shape,np.uint8)
                        mask[y-50:y+h+50,x-50:x+w+50] = frame[y-50:y+h+50,x-50:x+w+50]
                
                # frame = cv2.resize(frame, (1280, 720), interpolation=cv2.BORDER_DEFAULT)
                # cv2.imshow('my webcam', frame)
                # frame = cv2.Canny(frame, 50, 150)


                cam.send(mask)
                cam.sleep_until_next_frame()
            else:
                QtWidgets.QMessageBox.about(win, "Error", "Cannot read frame.")
                print("cannot read frame.")
                break
        cap.release()
    print("Thread end.")

def stop():
    global running
    running = False
    print("stoped..")

def start():
    global running
    running = True
    th = threading.Thread(target=run)
    th.start()
    print("started..")

def onExit():
    print("exit")
    stop()

app = QtWidgets.QApplication([])
win = QtWidgets.QWidget()
vbox = QtWidgets.QVBoxLayout()
label = QtWidgets.QLabel()
btn_start = QtWidgets.QPushButton("Camera On")
btn_stop = QtWidgets.QPushButton("Camera Off")
vbox.addWidget(label)
vbox.addWidget(btn_start)
vbox.addWidget(btn_stop)
win.setLayout(vbox)
win.show()

btn_start.clicked.connect(start)
btn_stop.clicked.connect(stop)
app.aboutToQuit.connect(onExit)

sys.exit(app.exec_())
