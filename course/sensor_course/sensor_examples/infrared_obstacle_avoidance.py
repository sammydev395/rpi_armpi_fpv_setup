#!/usr/bin/env python3
# coding=utf8
# 第15章 拓展课程之传感器开发与应用\1.拓展课程-传感器基础开发课\第3课 红外避障传感器检测(15. expanded course of sensor development and application\1. sensor basic development course\Lesson 3 infrared obstacle avoidance sensor detection)
import time
import gpiod
from common.ros_robot_controller_sdk import Board

board = Board()

## 初始化引脚模式(initialize pin mode)
chip = gpiod.chip("gpiochip4")
pin = chip.get_line(24) #BCM
config = gpiod.line_request()
config.consumer = "pin"
config.request_type = gpiod.line_request.DIRECTION_INPUT
pin.request(config)
    
detected = False
while True:
    if pin.get_value() == 0: # 读取引脚数字值(read pin numerical value)
        time.sleep(0.05)
        if pin.get_value() == 0:  # 读取引脚数字值(read pin numerical value)
            if not detected: #这里做一个判断，防止反复响(check to prevent repeated triggering)
                detected = True
                board.set_buzzer(1900, 0.1, 0.9, 1)# 设置蜂鸣器响0.1秒(set the buzzer to emit for 0.1 second)
    else:
        detected = False
