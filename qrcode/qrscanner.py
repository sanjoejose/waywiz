import cv2
from pyzbar.pyzbar import decode
import time

cam = cv2.VideoCapture(0)
cam.set(5, 640)
cam.set(6, 480)

camera = True
while camera == True:
    suceess, frame = cam.read()

    for i in decode(frame):
        print(i.type)
        j=int((i.data.decode('utf-8')))
        j=j/2
        print(j)
        time.sleep(6)

        cv2.imshow("OurQr_Code_Scanner", frame)   
        cv2.waitKey(3) 