#!/usr/bin/env python3
# coding=utf8
# 第15章 拓展课程之传感器开发与应用\2.拓展课程-传感器应用开发课程\第11课 机械臂触摸控制(15. expanded course of sensor development and application\1. sensor basic application course\Lesson 11 robotic arm touch control)
import os
import time
import gpiod
from common.ros_robot_controller_sdk import Board
from common.action_group_controller import ActionGroupController

board = Board()
acg = ActionGroupController(board, action_path=os.path.split(os.path.realpath(__file__))[0] + '/action_groups')

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
                acg.runAction('wave')
    else:
        pressed = False
