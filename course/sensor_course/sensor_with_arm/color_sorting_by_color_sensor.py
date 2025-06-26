#!/usr/bin/env python3
# coding=utf8
# 第15章 拓展课程之传感器开发与应用\2.拓展课程-传感器应用开发课程\第5课 机械臂颜色传感器识别(15. expanded course of sensor development and application\1. sensor basic application course\Lesson 5 robotic arm color sensor recognition)
import os
import time
import signal
from sensor.apds9960 import APDS9960
from common.yaml_handle import get_yaml_data
from common.ros_robot_controller_sdk import Board
from kinematics.kinematics_controller import KinematicsController

board = Board()
controller = KinematicsController(board)
data = get_yaml_data(os.path.join(os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], '../')), 'sensor_examples/color_sensor_calibration.yaml'))
board.bus_servo_set_position(0.5, [[1, 200]])
controller.go_pose_target([0.1, 0, 0.1], 45, [-90, 90], 0, 1)
time.sleep(1)

#颜色传感器初始化(color sensor initialization)
apds = APDS9960()
apds.enableLightSensor()
detect_color = None

start = True
#关闭前处理(process before closing)
def Stop(signum, frame):
    global start

    start = False
    print('关闭中...')

#先将所有灯关闭(turn off all lights)
board.set_rgb([[1, 0, 0, 0], [2, 0, 0, 0]])

signal.signal(signal.SIGINT, Stop)

while True:
    #读取三个颜色通道值(read three color channel values)
    red = apds.readRedLight()
    green = apds.readGreenLight()
    blue = apds.readBlueLight()
    
    #加入校准(incorporate calibration)
    r = abs(int((red - data['R_B'])*255/(data['R_W'] - data['R_B'])))
    g = abs(int((green - data['G_B'])*255/(data['G_W'] - data['G_B'])))
    b = abs(int((blue - data['B_B'])*255/(data['B_W'] - data['B_B'])))
    
    #判别颜色(color discrimination)
    if r - max(g, b) > 40:
        detect_color = 'red'
        board.set_rgb([[1, 255, 0, 0], [2, 255, 0, 0]])  #设置2个灯为红色(set two lights red)
        
        board.bus_servo_set_position(0.3, [[6, 400]])
        time.sleep(0.3)
        board.bus_servo_set_position(0.6, [[6, 600]])
        time.sleep(0.6)
        board.bus_servo_set_position(0.3, [[6, 500]])
        time.sleep(0.3)
        
    elif g - max(r, b) > 40:
        detect_color = 'green'
        print(detect_color)
        board.set_buzzer(1900, 0.1, 0.9, 1)# 设置蜂鸣器响0.1秒(set buzzer to emit for 0.1 second)
        board.set_rgb([[1, 0, 255, 0], [2, 0, 255, 0]])  #设置2个灯为绿色(set two lights green)
        time.sleep(1)
        board.bus_servo_set_position(0.5, [[1, 450]])
        time.sleep(1)
        board.bus_servo_set_position(2, [[6, 875]])
        time.sleep(2)
        controller.go_pose_target([0, 0.1, 0.01], 90, [-90, 90], 0, 1)
        time.sleep(1)
        board.bus_servo_set_position(0.5, [[1, 200]])
        time.sleep(1)
        controller.go_pose_target([0, 0.1, 0.1], 45, [-90, 90], 0, 1)
        time.sleep(1)
        controller.go_pose_target([0.1, 0, 0.1], 45, [-90, 90], 0, 2)
        time.sleep(2)
    elif b - max(r, g) > 40:
        detect_color = 'blue'
        board.set_buzzer(1900, 0.1, 0.9, 1)# 设置蜂鸣器响0.1秒(set buzzer to emit for 0.1 second)
        print(detect_color)
        board.set_rgb([[1, 0, 0, 255], [2, 0, 0, 255]])  #设置2个灯为蓝色(set two lights blue)
        time.sleep(1)
        board.bus_servo_set_position(0.5, [[1, 450]])
        time.sleep(1)
        board.bus_servo_set_position(2, [[6, 135]])
        time.sleep(2)
        controller.go_pose_target([0, -0.1, 0.01], 90, [-90, 90], 0, 1)
        time.sleep(1)
        board.bus_servo_set_position(0.5, [[1, 200]])
        time.sleep(1)
        controller.go_pose_target([0, -0.1, 0.1], 45, [-90, 90], 0, 1)
        time.sleep(1)
        controller.go_pose_target([0.1, 0, 0.1], 45, [-90, 90], 0, 2)
        time.sleep(2)
    else:
        detect_color = None
        board.set_rgb([[1, 50, 50, 50], [2, 50, 50, 50]]) #所有灯低亮度白色(all lights set to low brightness white)
    if not start:
        board.set_rgb([[1, 0, 0, 0], [2, 0, 0, 0]]) #所有灯关闭(turn off all lights)
        print('已关闭')
        break



