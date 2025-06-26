#!/usr/bin/python3
# coding=utf8
# 第12章 ROS+OpenCV课程\2.AI视觉追踪\第6课 AprilTag追踪(12. ROS+OpenCV course\2. AI vision tracking\Lesson 6 AprilTag tracking)
import cv2
import time
import numpy as np
from common import pid
from common import apriltag
from common.ros_robot_controller_sdk import Board
from kinematics.kinematics_controller import KinematicsController

x_dis = 500
y_dis = 0.10
Z_DIS = 0.18
z_dis = Z_DIS
x_pid = pid.PID(0.15, 0, 0)  # pid初始化(pid initialization)
y_pid = pid.PID(0.00001, 0, 0)
z_pid = pid.PID(0.00005, 0, 0)

#apriltag检测(apriltag detection)
board = Board()
controller = KinematicsController(board)
board.bus_servo_set_position(0.5, [[1, 200]])
controller.go_pose_target([y_dis, 0, z_dis], 0, [-90, 90], 0, 1)
time.sleep(1)

# 检测apriltag(detect apriltag)
detector = apriltag.Detector(searchpath=apriltag._get_demo_searchpath())
def apriltagDetect(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detections = detector.detect(gray, return_image=False)

    if len(detections) != 0:
        for detection in detections:                       
            corners = np.rint(detection.corners)  # 获取四个角点(get four angular points)
            cv2.drawContours(img, [np.array(corners, np.int)], -1, (0, 255, 255), 2)

            tag_family = str(detection.tag_family, encoding='utf-8')  # 获取tag_family(get tag_family)
            tag_id = int(detection.tag_id)  # 获取tag_id(get tag_id)

            x, y = int(detection.center[0]), int(detection.center[1])  # 中心点(center point)
            
            area = int(2*((corners[0][1] - detection.center[1])**2 + (corners[0][0] - detection.center[0])**2))
            return tag_family, tag_id, x, y, area
            
    return None, None, None, None, None

def run(img):
    global x_dis, y_dis, z_dis
    img_h, img_w = img.shape[:2]
    tag_family, tag_id, x, y, area = apriltagDetect(img) # apriltag检测(apriltag detection)
    
    if tag_id is not None:
        x_pid.SetPoint = img_w / 2.0  # 设定(setting)
        x_pid.update(x)  # 当前(current)
        x_dis += int(x_pid.output)  # 输出(output)

        x_dis = 0 if x_dis < 0 else x_dis
        x_dis = 1000 if x_dis > 1000 else x_dis

        y_pid.SetPoint = 6000  # 设定(setting)
        if abs(area - 6000) < 500:
            area = 6000
        y_pid.update(area)  # 当前(current)
        y_dis += y_pid.output  # 输出(output)
        y_dis = 0.05 if y_dis < 0.05 else y_dis
        y_dis = 0.10 if y_dis > 0.10 else y_dis
        
        z_pid.SetPoint = img_h / 2.0
        if abs(y - img_h/2.0) < 20:
            y = int(img_h/2.0)
            
        z_pid.update(y)
        z_dis += z_pid.output

        z_dis = 0.23 if z_dis > 0.23 else z_dis
        z_dis = 0.15 if z_dis < 0.15 else z_dis
        res = controller.set_pose_target([y_dis, 0, z_dis], 0, [-90, 90], 0)
        # print(area)
        if res[1]:
            board.bus_servo_set_position(0.02, [[3, res[1][3]], [4, res[1][2]], [5, res[1][1]], [6, x_dis]])
        cv2.putText(img, "({}, {}, {})".format(x, y, area), (x - int((1 + len(str(x)) + len(str(y)) + len(str(area)))*9), y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2)      
        cv2.putText(img, "tag_id: " + str(tag_id), (10, img.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, [0, 255, 255], 2)
        cv2.putText(img, "tag_family: " + tag_family, (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, [0, 255, 255], 2)
    else:
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
