#!/usr/bin/env python3
# coding=utf8
# 第15章 拓展课程之传感器开发与应用\1.拓展课程-传感器基础开发课\第6课 发光超声波RGB控制(15. expanded course of sensor development and application\1. sensor basic development course\Lesson 6 glowy ultrasonic RGB control)
import time
import signal
from sensor import ultrasonic_sensor

s = ultrasonic_sensor.Ultrasonic()
s.setRGBMode(0)      #设置灯的模式，0为彩灯模式，1为呼吸灯模式(set light mode, 0 indicates color light mode, 1 indicates breathing light mode)
s.setRGB(1, (0,0,0)) # 关闭两边RGB(close RGB in two sides)
s.setRGB(0, (0,0,0))
time.sleep(1)

start = True
#关闭前处理(process before closing)
def Stop(signum, frame):
    global start

    start = False
    print('关闭中...')

signal.signal(signal.SIGINT, Stop)

delay = 0
color = 'red'
while True:
    if time.time() > delay:
        if color == 'red':
            color = 'green'
            s.setRGBMode(0) #设置灯的模式，0为彩灯模式，1为呼吸灯模式(set light mode, 0 indicates color light mode, 1 indicates breathing light mode)
            s.setRGB(1, (255,0,0))  #两边RGB设置为红色(set RGB in two sides red)
            s.setRGB(0, (255,0,0))
            delay = time.time() + 2
        elif color == 'green':
            color = 'blue'
            s.setRGB(1, (0,255,0))  #两边RGB设置为绿色(set RGB in two sides green)
            s.setRGB(0, (0,255,0))
            delay = time.time() + 2
        elif color == 'blue':
            color = 'random'
            s.setRGB(1, (0,0,255))  #两边RGB设置为蓝色(set RGB in two sides blue)
            s.setRGB(0, (0,0,255))
            delay = time.time() + 2
        elif color == 'random':
            color = 'red'
            s.setBreathCycle(0, 0, 2000)
            s.setBreathCycle(1, 0, 2000)  # 设置超声波RGB颜色渐变模式(set ultrasonic RGB color to gradient mode)
            delay = time.time() + 5
    if not start:
        s.setRGBMode(0)
        s.setRGB(1, (0, 0, 0))  # 关闭两边RGB(close two sides RGB)
        s.setRGB(0, (0, 0, 0))
        print('已关闭')
        break
    
