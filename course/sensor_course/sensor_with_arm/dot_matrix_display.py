#!/usr/bin/env python3
# coding=utf8
# 第15章 拓展课程之传感器开发与应用\2.拓展课程-传感器应用开发课程\第8课 机械臂点阵显示(15. expanded course of sensor development and application\1. sensor basic application course\Lesson 8 robotic arm dot matrix display)
import os
from sensor import dot_matrix_sensor
from common.ros_robot_controller_sdk import Board
from common.action_group_controller import ActionGroupController

board = Board()
acg = ActionGroupController(board, action_path=os.path.split(os.path.realpath(__file__))[0] + '/action_groups')

dms = dot_matrix_sensor.TM1640(dio=24, clk=22)

## 显示'FPV'(display 'FPV')
lst = ['1111011110100001', 
       '1000010010100001',
       '1000010010100001',
       '1111011110100001',
       '1000010000100001',
       '1000010000100001',
       '1000010000010010',
       '1000010000001100']             

dms.set_buf_horizontal(lst)
dms.update_display()

acg.runAction('wave') # 参数为动作组的名称，不包含后缀，以字符形式传入(parameter as the name of action group, without suffix, input as character)
dms.clear()
