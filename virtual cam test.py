import sys
import cv2
import pyvirtualcam

xml = 'haarcascade_frontalface_alt2.xml'
face_cascade = cv2.CascadeClassifier(xml)

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
fmt = pyvirtualcam.PixelFormat.BGR
with pyvirtualcam.Camera(width=frame.shape[1], height=frame.shape[0], fps=30, fmt=fmt, print_fps=True) as cam:
    while True:
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray,1.05, 5)
        print("Number of faces detected: " + str(len(faces)))
        
        mask = frame
        mask = cv2.resize(mask, dsize=(0, 0), fx=0.1, fy=0.1) # 축소
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
        cv2.imshow('result1', mask)
        cv2.imshow('result', frame)
        cam.sleep_until_next_frame()
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cap.release()
    cv2.destroyAllWindows()


    
    # k = cv2.waitKey(30) & 0xff
    # if k == 27: # Esc 키를 누르면 종료
    #     break


