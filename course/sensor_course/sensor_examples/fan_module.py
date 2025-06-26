#!/usr/bin/env python3
# coding=utf8
# 第15章 拓展课程之传感器开发与应用\1.拓展课程-传感器基础开发课\第9课 风扇模块控制(15. expanded course of sensor development and application\1. sensor basic development course\Lesson 9 fan module control)
import time
import gpiod

## 初始化引脚模式(initialize pin mode)
chip = gpiod.chip("gpiochip4")
fanPin1 = chip.get_line(24)
fanPin2 = chip.get_line(22)
config = gpiod.line_request()
config.consumer = "pin1"
config.request_type = gpiod.line_request.DIRECTION_OUTPUT
fanPin1.request(config)

config = gpiod.line_request()
config.consumer = "pin2"
config.request_type = gpiod.line_request.DIRECTION_OUTPUT
fanPin2.request(config)

## 开启风扇, 顺时针(start fan, clockwise)
fanPin1.set_value(1)  # 设置引脚输出高电平(set pin output high voltage)
fanPin2.set_value(0)  # 设置引脚输出低电平(set pin output low voltage)

## 延时3秒(delay for 3 seconds)
time.sleep(3)

#逆时针(anticlockwise)
fanPin1.set_value(0)  
fanPin2.set_value(1)  

time.sleep(3)

## 关闭风扇(close fan)
fanPin1.set_value(0)  # 设置引脚输出高电平(set pin output high voltage)
fanPin2.set_value(0)  # 设置引脚输出低电平(set pin output low voltage)
