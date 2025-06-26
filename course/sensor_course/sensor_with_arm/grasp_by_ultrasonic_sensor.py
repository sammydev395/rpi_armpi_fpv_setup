#!/usr/bin/env python3
# coding=utf8
# 第15章 拓展课程之传感器开发与应用\2.拓展课程-传感器应用开发课程\第3课 机械臂超声波控制抓取(15. expanded course of sensor development and application\1. sensor basic application course\Lesson 3 ultrasonic control grasping)
import time
from sensor import ultrasonic_sensor
from common.ros_robot_controller_sdk import Board
from kinematics.kinematics_controller import KinematicsController

board = Board()
controller = KinematicsController(board)
board.bus_servo_set_position(0.5, [[1, 200]])
controller.go_pose_target([0.1, 0, 0.18], 0, [-90, 90], 0, 1)
time.sleep(1)

s = ultrasonic_sensor.Ultrasonic()
s.setBreathCycle(0, 0, 2000)
s.setBreathCycle(1, 0, 2000)  # 设置超声波RGB颜色渐变模式(set ultrasonic RGB color gradient mode)

while True:
    distance = s.getDistance() / 10
    print("Distance:", distance, "cm")
    if distance <= 15.0 :
        board.set_buzzer(1900, 0.1, 0.9, 1)# 设置蜂鸣器响0.1秒(set buzzer to emit for 0.1 second)
        time.sleep(1.5)
        board.bus_servo_set_position(0.5, [[1, 600]])
        time.sleep(1)
        controller.go_pose_target([0.12, 0, 0.01], -90, [-90, 90], 0, 2)
        time.sleep(2.2)
        board.bus_servo_set_position(0.5, [[1, 200]])
        time.sleep(0.5)
        controller.go_pose_target([0.1, 0, 0.18], 0, [-90, 90], 0, 2)
        time.sleep(2.2)
    else:
        time.sleep(0.1)
    
