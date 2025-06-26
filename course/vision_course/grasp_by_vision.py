#!/usr/bin/python3
# coding=utf8
# 第13章 ArmPi FPV创意玩法课程\1.AI视觉创意玩法\第3课 你放我抓(13. ArmPi FPV creative application course\1. AI vision creative programs\Lesson 3 intelligent transport)
import os
import cv2
import math
import time
import threading
import numpy as np
from common.yaml_handle import get_yaml_data
from common.ros_robot_controller_sdk import Board
from kinematics.kinematics_controller import KinematicsController

range_rgb = {
    'red':   (0, 0, 255),
    'blue':  (255, 0, 0),
    'green': (0, 255, 0),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'None': (0, 0, 0)}

board = Board()
controller = KinematicsController(board)
lab_data = get_yaml_data(os.path.join(os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], '../sensor_course/sensor_with_arm')), 'lab_config.yaml'))['color_range_list']
board.bus_servo_set_position(0.5, [[1, 200]])
controller.go_pose_target([0.1, 0, 0.1], 90, [-90, 90], 0, 1)
time.sleep(1)

#找出面积最大的轮廓(find out the contour with largest area)
#参数为要比较的轮廓的列表(the parameter is a list of contours to compare)
def getAreaMaxContour(contours):
        contour_area_temp = 0
        contour_area_max = 0
        area_max_contour = None

        for c in contours : #历遍所有轮廓(iterate through all contours)
            contour_area_temp = math.fabs(cv2.contourArea(c))  #计算轮廓面积(calculate contour area)
            if contour_area_temp > contour_area_max:
                contour_area_max = contour_area_temp
                if contour_area_temp > 300:  #只有在面积大于300时，最大面积的轮廓才是有效的，以过滤干扰(only when contours with an area greater than 300 are considered valid, and the contour with the maximum area is used to filter out interference)
                    area_max_contour = c
        return area_max_contour, contour_area_max  #返回最大的轮廓(return the largest contour)

#设置扩展板的RGB灯颜色使其跟要追踪的颜色一致(set the color of RGB light on the expansion board match to the tracking color)
def set_rgb(color):
    if color == "red":
        board.set_rgb([[1, 255, 0, 0], [2, 255, 0, 0]])
    elif color == "green":
        board.set_rgb([[1, 0, 255, 0], [2, 0, 255, 0]])
    elif color == "blue":
        board.set_rgb([[1, 0, 0, 255], [2, 0, 0, 255]])
    else:
        board.set_rgb([[1, 0, 0, 0], [2, 0, 0, 0]])

detect_color = 'None'
start_pick_up = False
def move():
    global detect_color
    global start_pick_up
    
    while True:
        if start_pick_up and detect_color != 'None':       
            board.set_buzzer(1900, 0.1, 0.9, 1)# 设置蜂鸣器响0.1秒(set buzzer to emit for 0.1 second)
            time.sleep(2)
            board.bus_servo_set_position(0.5, [[1, 450]])
            time.sleep(1)
            controller.go_pose_target([0, 0.1, 0.1], 90, [-90, 90], 0, 2)
            time.sleep(2)
            controller.go_pose_target([0, 0.12, 0.01], 90, [-90, 90], 0, 1)
            time.sleep(1.5)
            board.bus_servo_set_position(0.5, [[1, 200]])
            time.sleep(0.5)
            controller.go_pose_target([0, 0.1, 0.1], 90, [-90, 90], 0, 1)
            time.sleep(1)
            controller.go_pose_target([0.1, 0, 0.1], 90, [-90, 90], 0, 2)
            time.sleep(2)
            
            detect_color = 'None'
            start_pick_up = False
        else:
            time.sleep(0.01)
    
# 运行子线程(run sub threat)
th = threading.Thread(target=move)
th.setDaemon(True)
th.start()

def run(img):
    global start_pick_up
    global detect_color
        
    frame_gb = cv2.GaussianBlur(img, (3, 3), 3)
    frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)  # 将图像转换到LAB空间(convert the image to the LAB space)
    if not start_pick_up:
        if target_color in lab_data:
            frame_mask = cv2.inRange(frame_lab,
                                         (lab_data[target_color]['min'][0],
                                          lab_data[target_color]['min'][1],
                                          lab_data[target_color]['min'][2]),
                                         (lab_data[target_color]['max'][0],
                                          lab_data[target_color]['max'][1],
                                          lab_data[target_color]['max'][2]))  #对原图像和掩模进行位运算(perform bitwise operations on the original image and the mask)
            opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))  # 开运算(opening operation)
            closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))  # 闭运算(closing operation)
            contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # 找出轮廓(find out contour)
            areaMaxContour, area_max = getAreaMaxContour(contours)  # 找出最大轮廓(find out the largest contour)
        if area_max > 500:  # 有找到最大面积(the largest area is found)
            rect = cv2.minAreaRect(areaMaxContour)
            box = np.int0(cv2.boxPoints(rect))
            
            cv2.drawContours(img, [box], -1, range_rgb[target_color], 2)
            detect_color = target_color
            start_pick_up = True
            set_rgb(target_color)               
        else:
            detect_color = "None"
            set_rgb(detect_color)
    
    return img

if __name__ == '__main__':
    target_color = 'red'
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
