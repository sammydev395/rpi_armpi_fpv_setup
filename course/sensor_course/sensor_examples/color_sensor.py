#!/usr/bin/env python3
# coding=utf8
# 第15章 拓展课程之传感器开发与应用\1.拓展课程-传感器基础开发课\第2课 颜色传感器控制(15. expanded course of sensor development and application\1. sensor basic development course\Lesson 2 color sensor control)
import signal
from sensor.apds9960 import APDS9960
from common.yaml_handle import get_yaml_data
from common.ros_robot_controller_sdk import Board

board = Board()
data = get_yaml_data('color_sensor_calibration.yaml')

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

#先将所有灯关闭(turn off all the lights firstly)
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
        board.set_rgb([[1, 255, 0, 0], [2, 255, 0, 0]])  # 设置2个灯为红色(set two lights red)
    elif g - max(r, b) > 40:
        detect_color = 'green'
        board.set_rgb([[1, 0, 255, 0], [2, 0, 255, 0]])  # 设置2个灯为绿色(set two lights green)
    elif b - max(r, g) > 40:
        detect_color = 'blue'
        board.set_rgb([[1, 0, 0, 255], [2, 0, 0, 255]])  # 设置2个灯为蓝色(set two lights blue)
    else:
        detect_color = None
        board.set_rgb([[1, 50, 50, 50], [2, 50, 50, 50]])  # 所有灯低亮度白色(all lights dimmed to low brightness white)
    print(detect_color)
    
    if not start:
        board.set_rgb([[1, 0, 0, 0], [2, 0, 0, 0]])  # 所有灯关闭(turn all lights off)
        print('已关闭')
        break
