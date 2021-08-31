# -*- coding: utf-8 -*-
import cv2
import pyvirtualcam
import sys
import threading
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets


running = False
mosaicLevel = 100

def run():
    xml = 'haarcascade_eye.xml'
    face_cascade = cv2.CascadeClassifier(xml)

    global mosaicLevel

    _mosaic = (202-mosaicLevel)*0.001
    global running
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    fmt = pyvirtualcam.PixelFormat.BGR
    with pyvirtualcam.Camera(width=frame.shape[1], height=frame.shape[0], fps=30, fmt=fmt, print_fps=False) as cam:
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
                        mask[y-100:y+h+150,x-50:x+w+50] = frame[y-100:y+h+150,x-50:x+w+50]
                
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



class Ui_MainPage(object):
    def setupUi(self, MainPage):
        MainPage.setObjectName("MainPage")
        MainPage.resize(400, 300)
        
        self.slider_mosaic_level = QtWidgets.QSlider(MainPage)
        self.slider_mosaic_level.setGeometry(QtCore.QRect(20, 50, 131, 22))
        self.slider_mosaic_level.setOrientation(QtCore.Qt.Horizontal)
        self.slider_mosaic_level.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.slider_mosaic_level.setTickInterval(0)
        self.slider_mosaic_level.setObjectName("slider_mosaic_level")
        self.label = QtWidgets.QLabel(MainPage)
        self.label.setGeometry(QtCore.QRect(20, 20, 71, 16))
        self.label.setObjectName("label")
        self.btn_on = QtWidgets.QPushButton(MainPage)
        self.btn_on.setGeometry(QtCore.QRect(220, 50, 75, 23))
        self.btn_on.setDefault(False)
        self.btn_on.setObjectName("btn_on")
        self.label_on_off = QtWidgets.QLabel(MainPage)
        self.label_on_off.setGeometry(QtCore.QRect(260, 20, 71, 21))
        self.btn_quit = QtWidgets.QPushButton(MainPage)
        self.btn_quit.setGeometry(QtCore.QRect(260, 100, 75, 23))
        self.btn_on.setObjectName("btn_quit")

        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(16)
        self.label_on_off.setFont(font)
        self.label_on_off.setAlignment(QtCore.Qt.AlignCenter)
        self.label_on_off.setObjectName("label_on_off")
        self.spin_box_mosaic_level = QtWidgets.QSpinBox(MainPage)
        self.spin_box_mosaic_level.setGeometry(QtCore.QRect(160, 50, 42, 22))
        self.spin_box_mosaic_level.setObjectName("spin_box_mosaic_level")
        self.camera_label = QtWidgets.QLabel(MainPage)
        self.camera_label.setGeometry(QtCore.QRect(170, 110, 56, 12))
        self.camera_label.setText("")
        self.camera_label.setObjectName("camera_label")
        self.btn_off = QtWidgets.QPushButton(MainPage)
        self.btn_off.setGeometry(QtCore.QRect(300, 50, 75, 23))
        self.btn_off.setDefault(False)
        self.btn_off.setObjectName("btn_off")

        self.retranslateUi(MainPage)
        QtCore.QMetaObject.connectSlotsByName(MainPage)

    def retranslateUi(self, MainPage):
        global mosaicLevel

        _translate = QtCore.QCoreApplication.translate
        MainPage.setWindowTitle(_translate("MainPage", "Dialog"))
        self.label.setText(_translate("MainPage", "Mosaic level"))
        self.btn_on.setText(_translate("MainPage", "ON"))
        self.label_on_off.setText(_translate("MainPage", "OFF"))
        self.btn_off.setText(_translate("MainPage", "OFF"))
        self.btn_quit.setText(_translate("MainPage", "Quit"))

        # enable custom window hint
        MainPage.setWindowFlags(MainPage.windowFlags() | QtCore.Qt.CustomizeWindowHint)
        # disable (but not hide) close button
        MainPage.setWindowFlags(MainPage.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)

            # 화면에 있는 버튼과 스핀박스, 슬라이더 세팅
        self.btn_on.clicked.connect(self.btn_on_function)
        self.btn_off.clicked.connect(self.btn_off_function)
        self.btn_quit.clicked.connect(self.btn_quit_function)

        self.spin_box_mosaic_level.setRange(0, 200)
        self.spin_box_mosaic_level.setValue(mosaicLevel)

        self.spin_box_mosaic_level.valueChanged.connect(self.slider_mosaic_level.setValue)
        self.slider_mosaic_level.valueChanged.connect(self.spin_box_mosaic_level.setValue)
        
        self.slider_mosaic_level.valueChanged.connect(self.mosaic_level)

        self.slider_mosaic_level.setTickInterval(50)
        self.slider_mosaic_level.setTickPosition(QSlider.TicksBelow)
        self.slider_mosaic_level.setRange(0, 200)
        self.slider_mosaic_level.setValue(mosaicLevel)

        QMessageBox.about(MainWindow, "Warning", "If you have not installed OBS Studio, please download OBS Studio.")

    def mosaic_level(self):
        global mosaicLevel
        mosaicLevel = self.slider_mosaic_level.value()

    def btn_quit_function(self):
        global running
        running = False
        QtCore.QCoreApplication.instance().quit()
        sys.exit(app.exec_())

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


if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainPage()
    ui.setupUi(MainWindow)


    MainWindow.show()

    sys.exit(app.exec_())

win = QtWidgets.QWidget()