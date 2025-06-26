#!/usr/bin/env python3
# coding=utf8
# 第15章 拓展课程之传感器开发与应用\1.拓展课程-传感器基础开发课\第8课 数码管显示(15. expanded course of sensor development and application\1. sensor basic development course\Lesson 8 digital tube display)
import time
from sensor import dot_matrix_sensor
from sensor import ultrasonic_sensor

dms = dot_matrix_sensor.TM1640(dio=24, clk=22)

s = ultrasonic_sensor.Ultrasonic()
# 设置超声波RGB颜色渐变模式(set ultrasonic RGB color to gradient mode)
s.setBreathCycle(0, 0, 2000)
s.setBreathCycle(1, 0, 2000)

while True:
    distance = s.getDistance()/10 #获取超声波测距数据,单位cm(get ultrasonic distance measurement, with unit in centimeter)
    print('dist:',distance)
    dms.set_number(distance)
    dms.update_display()
    time.sleep(0.1)
