#!/usr/bin/env python3
# coding=utf8
# 第15章 拓展课程之传感器开发与应用\1.拓展课程-传感器基础开发课\第5课 发光超声波测距(15. expanded course of sensor development and application\1. sensor basic development course\Lesson 5 ultrasonic distance measurement)
import time
import signal
from sensor import ultrasonic_sensor
from common.ros_robot_controller_sdk import Board

board = Board()

s = ultrasonic_sensor.Ultrasonic()
# 设置超声波RGB颜色渐变模式(set ultrasonic RGB color to gradient mode)
s.setBreathCycle(0, 0, 2000)
s.setBreathCycle(1, 0, 2000) 

start = True
#关闭前处理(process before closing)
def Stop(signum, frame):
    global start

    start = False
    print('关闭中...')

signal.signal(signal.SIGINT, Stop)

while True:
    distance = s.getDistance() / 10  # 获取超声波测距数据,单位cm(get ultrasonic distance measurement with unit in centimeter)
    if distance <= 15.0:
        board.set_buzzer(1900, 0.05, 0.05, 1)# 设置蜂鸣器响0.1秒(set buzzer emits for 0.1 second)
    
    print("Distance:", distance)
    time.sleep(0.1)
    if not start:
        s.setRGBMode(0)
        print('已关闭')
        break
    
