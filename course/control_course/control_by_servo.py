#!/usr/bin/python3
# coding=utf8
# 第8章 ArmPi FPV逆运动学基础及实战应用课程/第3课 单次控制多个舵机(8. ArmPi FPV inverse kinematics basics & application course/Lesson 3 multiple servos control)
import time
from common.ros_robot_controller_sdk import Board

board = Board()
board.bus_servo_set_position(0.5, [[1, 200]])
time.sleep(1)
board.bus_servo_set_position(0.5, [[1, 700]])
time.sleep(1)
board.bus_servo_set_position(0.5, [[1, 300]])
time.sleep(1)

board.bus_servo_set_position(0.5, [[2, 200], [3, 700]])
time.sleep(1)
board.bus_servo_set_position(0.5, [[2, 800], [3, 500]])
time.sleep(1)
board.bus_servo_set_position(0.5, [[2, 500], [3, 200]])
time.sleep(1)

board.bus_servo_set_position(0.5, [[4, 550]])
time.sleep(1)
board.bus_servo_set_position(0.5, [[4, 800]])
time.sleep(1)

board.bus_servo_set_position(0.5, [[5, 800]])
time.sleep(1)
board.bus_servo_set_position(0.5, [[5, 500]])
time.sleep(1)
board.bus_servo_set_position(0.5, [[5, 650]])
time.sleep(1)

board.bus_servo_set_position(0.5, [[6, 200]])
time.sleep(1)
board.bus_servo_set_position(1, [[6, 800]])
time.sleep(1)
board.bus_servo_set_position(0.5, [[6, 500]])
time.sleep(1)
