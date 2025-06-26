#!/usr/bin/python3
# coding=utf8
# 第12章 ROS+OpenCV课程\2.AI视觉追踪\第2课 色块追踪实验(12. ROS+OpenCV course\2. AI vision tracking\Lesson 2 color tracking)
import os
import cv2
import math
import time
import numpy as np
from common import pid
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

x_dis = 500
y_dis = 0.10
Z_DIS = 0.18
z_dis = Z_DIS
x_pid = pid.PID(0.15, 0, 0)  # pid初始化(pid initialization)
y_pid = pid.PID(0.000003, 0, 0)
z_pid = pid.PID(0.00005, 0, 0)

board = Board()
controller = KinematicsController(board)
board.bus_servo_set_position(0.5, [[1, 200]])
controller.go_pose_target([y_dis, 0, z_dis], 0, [-90, 90], 0, 1)
lab_data = get_yaml_data(os.path.join(os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], '../sensor_course/sensor_with_arm')), 'lab_config.yaml'))['color_range_list']
time.sleep(1)
    
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

# 找出面积最大的轮廓(find out the contour with the largest area)
# 参数为要比较的轮廓的列表(the parameter is a list of contours to compare.)
def getAreaMaxContour(contours):
    
    contour_area_temp = 0
    contour_area_max = 0
    area_max_contour = None

    for c in contours:  # 历遍所有轮廓(iterate through all contours)
        contour_area_temp = math.fabs(cv2.contourArea(c))  # 计算轮廓面积(calculate contour area)
        if contour_area_temp > contour_area_max:
            contour_area_max = contour_area_temp
            if contour_area_temp > 300:  # 只有在面积大于300时，最大面积的轮廓才是有效的，以过滤干扰(only when contours with an area greater than 300 are considered valid, and the contour with the maximum area is used to filter out interference)
                area_max_contour = c

    return area_max_contour, contour_area_max  # 返回最大的轮廓(return the largest contour)

def run(img):
    global x_dis, y_dis, z_dis

    img_h, img_w = img.shape[:2]
    frame_gb = cv2.GaussianBlur(img, (3, 3), 3)
    frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)  # 将图像转换到LAB空间(convert the image to the LAB space)
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
            (x, y), r = cv2.minEnclosingCircle(areaMaxContour)
            
            cv2.circle(img, (int(x), int(y)), int(r), (0, 255, 255), 2)
            set_rgb(target_color)
      
            x_pid.SetPoint = img_w / 2.0  # 设定(setting)
            x_pid.update(x)  # 当前(current)
            x_dis += int(x_pid.output)  # 输出(output)

            x_dis = 0 if x_dis < 0 else x_dis
            x_dis = 1000 if x_dis > 1000 else x_dis
            y_pid.SetPoint = 6000  # 设定(setting)
            if abs(area_max - 6000) < 500:
                area_max = 6000
            y_pid.update(area_max)  # 当前(current)
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
            if res[1]:
                board.bus_servo_set_position(0.02, [[3, res[1][3]], [4, res[1][2]], [5, res[1][1]], [6, x_dis]])

    return img

if __name__ == '__main__':
    cap = cv2.VideoCapture(-1) #读取摄像头(read camera)
    target_color = 'red'
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
        
