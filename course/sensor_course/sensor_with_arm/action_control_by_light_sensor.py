#!/usr/bin/env python3
# coding=utf8
# 第15章 拓展课程之传感器开发与应用\2.拓展课程-传感器应用开发课程\第10课 机械臂感光控制(15. expanded course of sensor development and application\1. sensor basic application course\Lesson 10 robotic arm light control)
import os
import time
import gpiod
from common.ros_robot_controller_sdk import Board
from common.action_group_controller import ActionGroupController

board = Board()
acg = ActionGroupController(board, action_path=os.path.split(os.path.realpath(__file__))[0] + '/action_groups')

## 初始化引脚模式(initialize pin mode)
chip = gpiod.chip("gpiochip4")
light = chip.get_line(24) # BCM
config = gpiod.line_request()
config.consumer = 'light'
config.request_type = gpiod.line_request.DIRECTION_INPUT
light.request(config)

dark = False
while True:
    if light.get_value() == 1: # 读取引脚数字值(read pin numerical value)
        time.sleep(0.05)
        if light.get_value() == 1:
            if not dark:  # 这里做一个判断，防止反复响(check to prevent repeated triggering)
                dark = True
                board.set_buzzer(1900, 0.1, 0.9, 1)  # 设置蜂鸣器响0.1秒(set buzzer to emit for 0.1 second)
                acg.runAction('wave')
    else:
        dark = False
