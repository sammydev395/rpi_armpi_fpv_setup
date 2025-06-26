#!/usr/bin/env python3
# coding=utf8
# 第15章 拓展课程之传感器开发与应用\1.拓展课程-传感器基础开发课\第4课 触摸传感器检测(15. expanded course of sensor development and application\1. sensor basic development course\Lesson 4 touch sensor detection)
import time
import gpiod
from common.ros_robot_controller_sdk import Board

board = Board()

## 初始化引脚模式(initialize pin mode)
chip = gpiod.chip("gpiochip4")
touch = chip.get_line(24) #BCM
config = gpiod.line_request()
config.consumer = 'touch'
config.request_type = gpiod.line_request.DIRECTION_INPUT
touch.request(config)

pressed = False
while True:
    if touch.get_value() == 0: # 读取引脚数字值(read pin numerical value)
        time.sleep(0.05)
        if touch.get_value() == 0:
            if not pressed:  # 这里做一个判断，防止反复响(check to prevent repeated triggering)
                pressed = True
                board.set_buzzer(1900, 0.1, 0.9, 1)  # 设置蜂鸣器响0.1秒(set buzzer to emit for 0.1 second)
    else:
        pressed = False
