#!/usr/bin/python3
# coding=utf8
# 第15章 拓展课程之传感器开发与应用\2.拓展课程-传感器应用开发课程\第7课 机械臂颜色+AI识别(15. expanded course of sensor development and application\1. sensor basic application course\Lesson 7 robotic arm color+AI recognition)
import os
import cv2
import time
import math
import threading
import numpy as np
from sensor.apds9960 import APDS9960
from common.yaml_handle import get_yaml_data
from common.ros_robot_controller_sdk import Board
from kinematics.kinematics_controller import KinematicsController

board = Board()
controller = KinematicsController(board)
data = get_yaml_data(os.path.join(os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], '../')), 'sensor_examples/color_sensor_calibration.yaml'))
lab_data = get_yaml_data(os.path.join(os.path.split(os.path.realpath(__file__))[0], 'lab_config.yaml'))['color_range_list']
init_x, init_y, init_z = 0.1, 0, 0.05

def initMove():
    board.bus_servo_set_position(0.5, [[1, 200]])
    controller.go_pose_target([0.1, 0, 0.05], 90, [-90, 90], 0, 1)
    time.sleep(1)

#颜色传感器初始化(color sensor initialization)
apds = APDS9960()
apds.enableLightSensor()

range_rgb = {
    'red':   (0, 0, 255),
    'blue':  (255, 0, 0),
    'green': (0, 255, 0),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'None': (0, 0, 0),}

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

# 找出面积最大的轮廓(find out the largest contour)
# 参数为要比较的轮廓的列表(the parameter is a list of contours to compare)
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

detect_color = 'None'
status = 'detect'
rect = None
block_angle = 0
start_pick_up = False

# 获取旋转的角度(get rotation angle)
# 参数：机械臂末端坐标, 木块旋转角(parameter: End-effector coordinates of the robotic arm, rotation angle of the wooden block)
def getAngle(x, y, angle):
    theta6 = round(math.degrees(math.atan2(abs(x), abs(y))), 1)
    angle = abs(angle)
    
    if x < 0:
        if y < 0:
            angle1 = -(90 + theta6 - angle)
        else:
            angle1 = theta6 - angle
    else:
        if y < 0:
            angle1 = theta6 + angle
        else:
            angle1 = 90 - theta6 - angle

    if angle1 > 0:
        angle2 = angle1 - 90
    else:
        angle2 = angle1 + 90

    if abs(angle1) < abs(angle2):
        return angle1
    else:
        return angle2

def pick():
    global status
    global block_angle
    global detect_color
    global start_pick_up
    global init_x, init_y, init_z
    
    #放置坐标(placement coordinate)
    coordinate = {
        'red':   [0.12, -0.15, 0.015],
        'green': [0.06, -0.15, 0.015],
        'blue':  [0, -0.15, 0.015]}
    
    servo1 = 500
    
    while True:
        if status == 'detect':
            #读取三个颜色通道值(read three color channels)
            red = apds.readRedLight()
            green = apds.readGreenLight()
            blue = apds.readBlueLight()
            #加入校准(incorporate calibration)
            r = abs(int((red - data['R_B'])*255/(data['R_W'] - data['R_B'])))
            g = abs(int((green - data['G_B'])*255/(data['G_W'] - data['G_B'])))
            b = abs(int((blue - data['B_B'])*255/(data['B_W'] - data['B_B'])))
            #判别颜色(color discrimination)
            status = 'pick up'
            if r - max(g, b) > 40:
                detect_color = 'red'
            elif g - max(r, b) > 40:
                detect_color = 'green'
            elif b - max(r, g) > 40:
                detect_color = 'blue'
            else:
                status = 'detect'
                detect_color = 'None'
            if detect_color != 'None':
                board.set_buzzer(1900, 0.1, 0.9, 1)# 设置蜂鸣器响0.1秒(set the buzzer to emit for 0.1 second)
                print(detect_color)
        elif status == 'pick up' and start_pick_up:  
            set_rgb(detect_color)
            board.set_buzzer(1900, 0.1, 0.9, 1)# 设置蜂鸣器响0.1秒(set a buzzer to emit for 0.1 second)
            time.sleep(1) 
            board.bus_servo_set_position(0.5, [[1, servo1 - 280]])  # 爪子张开(open claw)
            time.sleep(0.5)

            controller.go_pose_target([init_x, init_y, 0.01], 90, [-90, 90], block_angle, 1)
            time.sleep(1.5)

            board.bus_servo_set_position(0.5, [[1, servo1]])  #夹持器闭合(close gripper)
            time.sleep(0.8)

            controller.go_pose_target([init_x, init_y, 0.12], 90, [-90, 90], 0, 1) #机械臂抬起(lift robotic arm)
            time.sleep(1)
        
            controller.go_pose_target([coordinate[detect_color][0], coordinate[detect_color][1], 0.12], 90, [-90, 90], 0, 1)
            time.sleep(1)
            
            controller.go_pose_target([coordinate[detect_color][0], coordinate[detect_color][1], coordinate[detect_color][2] + 0.003], 90, [-90, 90], 0, 1)
            time.sleep(0.5)

            angle = getAngle(coordinate[detect_color][0], coordinate[detect_color][1], -90)
            servo2_pulse = int(500 + round(angle * 1000 / 240))
            board.bus_servo_set_position(0.5, [[2, servo2_pulse]])
            time.sleep(0.5)
            
            controller.go_pose_target(coordinate[detect_color], 90, [-90, 90], angle, 1)       
            time.sleep(0.8)

            board.bus_servo_set_position(0.5, [[1, servo1 - 200]])  # 爪子张开  ，放下物体(open claw, put down object)
            time.sleep(0.8)

            controller.go_pose_target([coordinate[detect_color][0], coordinate[detect_color][1], 0.12], 90, [-90, 90], 0, 1)
            time.sleep(0.8)

            initMove()  # 回到初始位置(return to the initial position)
            init_x, init_y, init_z = 0.1, 0, 0.05
            detect_color = 'None'
            start_pick_up = False
            status = 'detect'
            set_rgb(detect_color)
        else:    
            time.sleep(0.01)
          
#运行子线程(run sub threat)
th = threading.Thread(target=pick)
th.setDaemon(True)
th.start()    

last_t = 0
def run(img):
    global last_t
    global start_pick_up
    global block_angle
    global init_x, init_y, init_z
    
    if detect_color != 'None' and not start_pick_up:
        frame_gb = cv2.GaussianBlur(img, (3, 3), 3)
        frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)  # 将图像转换到LAB空间(convert the image to the LAB space)
        color_area_max = None
        max_area = 0
        areaMaxContour_max = 0
        if detect_color in lab_data:
            frame_mask = cv2.inRange(frame_lab,
                                         (lab_data[detect_color]['min'][0],
                                          lab_data[detect_color]['min'][1],
                                          lab_data[detect_color]['min'][2]),
                                         (lab_data[detect_color]['max'][0],
                                          lab_data[detect_color]['max'][1],
                                          lab_data[detect_color]['max'][2]))  #对原图像和掩模进行位运算(perform bitwise operation on the original image and the mask)
            opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))  # 开运算(opening operation)
            closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))  # 闭运算(closing operation)
            contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # 找出轮廓(find out contour)
            areaMaxContour, area_max = getAreaMaxContour(contours)  # 找出最大轮廓(find out the largest contour)
            
            if areaMaxContour is not None:
                if area_max > max_area:  # 找最大面积(find the largest area)
                    max_area = area_max
                    color_area_max = detect_color
                    areaMaxContour_max = areaMaxContour
        
        if max_area > 500:  # 有找到最大面积(the largest area is found)
            rect = cv2.minAreaRect(areaMaxContour_max)
            box = np.int0(cv2.boxPoints(rect))
            cv2.drawContours(img, [box], -1, range_rgb[color_area_max], 2)
            x = int((box[0][0] + box[2][0])/2)
            y = int((box[0][1] + box[2][1])/2)
            cv2.circle(img, (x, y), 5, (0, 255, 255), -1)
            if y < 385:
                init_x += 0.001
                st1 = False
            elif y > 415:
                init_x -= 0.001
                st1 = False
            else:
                st1 = True
            if x < 305:
                init_y += 0.001
                st2 = False
            elif x > 335:
                init_y -= 0.001
                st2 = False
            else:
                st2 = True
            if st1 and st2:
                start_pick_up = True
                block_angle = int(rect[2])
            controller.go_pose_target([init_x, init_y, init_z], 90, [-90, 90], 0, 0.05)
        draw_color = range_rgb[detect_color]    
        cv2.putText(img, "Color: " + detect_color, (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, draw_color, 2)
    return img

    
if __name__ == '__main__':
    print('loading......')
    cap = cv2.VideoCapture(-1) #读取摄像头(read camera)
    print('loading completed!')
    initMove()
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
