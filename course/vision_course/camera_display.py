#!/usr/bin/python3
# coding=utf8
import cv2
import time

cap = cv2.VideoCapture(-1) #读取摄像头(read camera)
while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    else:
        time.sleep(0.01)
cap.release()
cv2.destroyAllWindows()
