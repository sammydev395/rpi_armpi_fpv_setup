#!/usr/bin/env python3
# coding=utf8
# 第15章 拓展课程之传感器开发与应用\2.拓展课程-传感器应用开发课程\第6课 机械臂超声波补光(15. expanded course of sensor development and application\1. sensor basic application course\Lesson 6 ultrasonic fill light)
import time
from sensor import ultrasonic_sensor

s = ultrasonic_sensor.Ultrasonic()
s.setRGBMode(0) #设置灯的模式，0为彩灯模式，1为呼吸灯模式(set light mode, 0 indicates color light mode, 1 indicates breathing light mode)
s.setRGB(1, (0, 0, 0)) # 关闭两边RGB(close the RGB in two sides)
s.setRGB(0, (0, 0, 0))
time.sleep(1)

s.setRGB(1, (255, 255, 255))  #两边RGB设置为白色(set the RGB in two sides to white)
s.setRGB(0, (255, 255, 255))

