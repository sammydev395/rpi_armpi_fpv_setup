#!/usr/bin/python3
# coding=utf8
import os
import time
import gpiod
from common.ros_robot_controller_sdk import Board
from common.action_group_controller import ActionGroupController

board = Board()
acg = ActionGroupController(board, action_path=os.path.split(os.path.realpath(__file__))[0] + '/action_groups')

try:
    key1_pin = 13
    chip = gpiod.chip("gpiochip4")

    key1 = chip.get_line(key1_pin)
    config = gpiod.line_request()
    config.consumer = "key1"
    config.request_type = gpiod.line_request.DIRECTION_INPUT
    config.flags = gpiod.line_request.FLAG_BIAS_PULL_UP
    key1.request(config)
except:
    print('按键默认被hw_button_scan占用，需要先关闭服务')
    print('sudo systemctl stop hw_button_scan.service')
key1_pressed = False
while True:
    if key1.get_value() == 0:
        time.sleep(0.05)
        if key1.get_value() == 0:
            if key1_pressed == False:
                key1_pressed = True
                print('start action')
                acg.runAction('wave')
        else:               
            key1_pressed = False
    else:
        key1_pressed = False



