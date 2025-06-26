#!/usr/bin/python3
# coding=utf8
# 第12章 ROS+OpenCV课程\1.AI视觉识别\第3课 AprilTag识别(12. Ros+OpenCV course\1. AI vision recognition\Lesson 3 AprilTag recognition)
import cv2
import math
import time
import numpy as np
from common import apriltag
from common.ros_robot_controller_sdk import Board

#apriltag检测(apriltag detection)
board = Board()
# 检测apriltag(detect apriltag)
detector = apriltag.Detector(searchpath=apriltag._get_demo_searchpath())
def apriltagDetect(img):   
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detections = detector.detect(gray, return_image=False)

    if len(detections) != 0:
        for detection in detections:                       
            corners = np.rint(detection.corners)  # 获取四个角点(obtain four angular point)
            cv2.drawContours(img, [np.array(corners, np.int)], -1, (0, 255, 255), 2)

            tag_family = str(detection.tag_family, encoding='utf-8')  # 获取tag_family(get tag_family)
            tag_id = int(detection.tag_id)  # 获取tag_id(get tag_id)

            return tag_family, tag_id
            
    return None, None

state = True
def run(img):
    global state
     
    tag_family, tag_id = apriltagDetect(img) # apriltag检测(apriltag detection)
    
    if tag_id is not None:
        if state:
            board.set_buzzer(1900, 0.1, 0.9, 1)# 设置蜂鸣器响0.1秒(set buzzer to emit for 0.1 second)
            state = False
        
        cv2.putText(img, "tag_id: " + str(tag_id), (10, img.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, [0, 255, 255], 2)
        cv2.putText(img, "tag_family: " + tag_family, (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, [0, 255, 255], 2)
    else:
        state = True
        cv2.putText(img, "tag_id: None", (10, img.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, [0, 255, 255], 2)
        cv2.putText(img, "tag_family: None", (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, [0, 255, 255], 2)
    
    return img

if __name__ == '__main__':
    cap = cv2.VideoCapture(-1) #读取摄像头(read camera)
    while True:
        ret, img = cap.read()
        if ret:
            frame = run(img)           
            cv2.imshow('frame', frame)
            key = cv2.waitKey(1)
            if key == 27:
                break
        else:
            time.sleep(0.01)
    cap.release()
    cv2.destroyAllWindows()
