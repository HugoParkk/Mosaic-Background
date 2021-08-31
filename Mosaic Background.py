import cv2
import pyvirtualcam
import sys
import threading
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import uic

running = False
mosaicLevel = 100

form_class = uic.loadUiType("Mosaic Background.ui")[0]

def run():
    xml = 'haarcascade_frontalface_alt2.xml'
    face_cascade = cv2.CascadeClassifier(xml)

    global mosaicLevel
    _mosaic = mosaicLevel*0.0004
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
                # print("Number of faces detected: " + str(len(faces)))
                
                mask = frame
                mask = cv2.resize(mask, dsize=(0, 0), fx=_mosaic, fy=_mosaic) # 축소
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
                # print("cannot read frame.")
                break
        cap.release()
        cam.close()
    # print("Thread end.")

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    
    global mosaicLevel
    
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Mosaic Background')

        # 화면에 있는 버튼과 스핀박스, 슬라이더 세팅
        self.btn_on.clicked.connect(self.btn_on_function)
        self.btn_off.clicked.connect(self.btn_off_function)

        self.spin_box_mosaic_level.valueChanged.connect(self.slider_mosaic_level.setValue)
        self.slider_mosaic_level.valueChanged.connect(self.spin_box_mosaic_level.setValue)

        self.spin_box_mosaic_level.setRange(0, 200)
        self.spin_box_mosaic_level.setValue(mosaicLevel)

        self.slider_mosaic_level.setTickInterval(50)
        self.slider_mosaic_level.setTickPosition(QSlider.TicksBelow)
        self.slider_mosaic_level.setRange(0, 200)
        self.slider_mosaic_level.setValue(mosaicLevel)

        QMessageBox.about(self, "Warning", "If you have not installed OBS Studio, you should install it quickly.")


    def btn_off_function(self):
        global running
        running = False
        self.label_on_off.setText('OFF')
        # print("stoped..")

    def btn_on_function(self):
        
        global running
        running = True
        th = threading.Thread(target=run)
        th.start()
        self.label_on_off.setText('ON')
        # print("started..")

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()

win = QtWidgets.QWidget()