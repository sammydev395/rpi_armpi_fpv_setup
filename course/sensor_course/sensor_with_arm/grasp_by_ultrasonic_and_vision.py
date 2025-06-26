#!/usr/bin/python3
# coding=utf8
# 第15章 拓展课程之传感器开发与应用\2.拓展课程-传感器应用开发课程\第4课 机械臂超声波+AI识别控制抓取(15. expanded course of sensor development and application\1. sensor basic application course\Lesson 4 ultrasonic + AI recognition control grasping)
import os
import cv2
import time
import math
import threading
import numpy as np
from common import yaml_handle
from sensor import ultrasonic_sensor
from common.ros_robot_controller_sdk import Board
from kinematics.kinematics_controller import KinematicsController

board = Board()
controller = KinematicsController(board)
s = ultrasonic_sensor.Ultrasonic()
s.setRGBMode(0)
s.setRGB(1, (0,0,0))
s.setRGB(0, (0,0,0))

# 初始位置(initial position)
def initMove():
    board.bus_servo_set_position(0.5, [[1, 200]])
    controller.go_pose_target([0.1, 0, 0.1], 90, [-90, 90], 0, 1)

range_rgb = {
    'red':   (0, 0, 255),
    'blue':  (255, 0, 0),
    'green': (0, 255, 0),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
}

target_color = None
lab_data = None
def load_config():
    global lab_data
    
    lab_data = yaml_handle.get_yaml_data(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'lab_config.yaml'))['color_range_list']

#找出面积最大的轮廓(find out the contour with largest area)
#参数为要比较的轮廓的列表(the parameter is a list of contours to be compared)
def getAreaMaxContour(contours) :
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

#设置扩展板的RGB灯颜色使其跟要追踪的颜色一致(set the color of RGB light on the expansion board to match the tracking color)
def set_rgb(color):
    if color == "red":
        board.set_rgb([[1, 255, 0, 0], [2, 255, 0, 0]])
    elif color == "green":
        board.set_rgb([[1, 0, 255, 0], [2, 0, 255, 0]])
    elif color == "blue":
        board.set_rgb([[1, 0, 0, 255], [2, 0, 0, 255]])
    else:
        board.set_rgb([[1, 0, 0, 0], [2, 0, 0, 0]])

color_list = []
detect_color = 'None'
start_pick_up = False

def init():
    load_config()
    initMove()

draw_color = range_rgb["black"]

detected = False
def move():
    global detected
    global detect_color
    global start_pick_up
    
    while True:
        if not start_pick_up:
            distance = s.getDistance() / 10
            print("Distance:", distance, "cm")
            if distance <= 15.0:
                detected = True
                board.set_buzzer(1900, 0.1, 0.9, 1)# 设置蜂鸣器响0.1秒(set the buzzer to emit for 0.1 second)
            time.sleep(1)
        elif start_pick_up and detect_color != 'None':
            if detect_color == target_color:
                board.set_buzzer(1900, 0.1, 0.9, 1)# 设置蜂鸣器响0.1秒(set the buzzer to emit for 0.1 second)
                time.sleep(1.5)
                board.bus_servo_set_position(0.5, [[1, 450]])
                time.sleep(1)
                controller.go_pose_target([0.12, 0, 0.01], 90, [-90, 90], 0, 2)
                time.sleep(2.2)
                board.bus_servo_set_position(0.5, [[1, 200]])
                time.sleep(0.5)
                controller.go_pose_target([0.1, 0, 0.1], 90, [-90, 90], 0, 2)
                time.sleep(2.2)
            else:
                board.bus_servo_set_position(0.3, [[2, 600]])
                time.sleep(0.3)
                board.bus_servo_set_position(0.5, [[2, 400]])
                time.sleep(0.5)
                board.bus_servo_set_position(0.5, [[2, 500]])
                time.sleep(0.3)
            detected = False
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
    global detect_color, draw_color, color_list
        
    if not detected:
        return img
    frame_gb = cv2.GaussianBlur(img, (3, 3), 3)
    frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)  # 将图像转换到LAB空间(convert the image to the LAB space)
    color_area_max = None
    max_area = 0
    areaMaxContour_max = 0
    if not start_pick_up:
        for i in __target_color:
            if i in lab_data:
                frame_mask = cv2.inRange(frame_lab,
                                             (lab_data[i]['min'][0],
                                              lab_data[i]['min'][1],
                                              lab_data[i]['min'][2]),
                                             (lab_data[i]['max'][0],
                                              lab_data[i]['max'][1],
                                              lab_data[i]['max'][2]))  #对原图像和掩模进行位运算(perform bitwise operation on the original image and the mask)
                opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))  # 开运算(opening operation)
                closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))  # 闭运算(closing operation)
                contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # 找出轮廓(find out contour)
                areaMaxContour, area_max = getAreaMaxContour(contours)  # 找出最大轮廓(find out the largest contour)
                if areaMaxContour is not None:
                    if area_max > max_area:  # 找最大面积(find the largest area)
                        max_area = area_max
                        color_area_max = i
                        areaMaxContour_max = areaMaxContour
        if max_area > 500:  # 有找到最大面积(the largest area is found)
            rect = cv2.minAreaRect(areaMaxContour_max)
            box = np.int0(cv2.boxPoints(rect))
            
            cv2.drawContours(img, [box], -1, range_rgb[color_area_max], 2)
            if color_area_max == 'red':  # 红色最大(maximum red)
                color = 1
            elif color_area_max == 'green':  # 绿色最大(maximum green)
                color = 2
            elif color_area_max == 'blue':  # 蓝色最大(maximum blue)
                color = 3
            else:
                color = 0
            color_list.append(color)
            if len(color_list) == 5:  # 多次判断(multiple evaluation)
                # 取平均值(read average value)
                color = int(round(np.mean(np.array(color_list))))
                color_list = []
                if color == 1:
                    start_pick_up = True
                    detect_color = 'red'
                    set_rgb(detect_color)
                    draw_color = range_rgb["red"]
                elif color == 2:
                    start_pick_up = True
                    detect_color = 'green'
                    set_rgb(detect_color)
                    draw_color = range_rgb["green"]
                elif color == 3:
                    start_pick_up = True
                    detect_color = 'blue'
                    set_rgb(detect_color)
                    draw_color = range_rgb["blue"]
                else:
                    start_pick_up = False
                    detect_color = 'None'
                    set_rgb(detect_color)
                    draw_color = range_rgb["black"]               
        else:
            draw_color = (0, 0, 0)
            detect_color = "None"
    
    cv2.putText(img, "Color: " + detect_color, (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, draw_color, 2)
    
    return img

if __name__ == '__main__':
    init()
    target_color = 'red'
    __target_color = ['red', 'green', 'blue']
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
