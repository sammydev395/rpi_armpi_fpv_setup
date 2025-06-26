#!/usr/bin/env python3
# coding=utf8
# 第15章 拓展课程之传感器开发与应用\1.拓展课程-传感器基础开发课\第7课 点阵模块显示(15. expanded course of sensor development and application\1. sensor basic development course\Lesson 7 dot matrix module display)
import time
from sensor import dot_matrix_sensor

dms = dot_matrix_sensor.TM1640(dio=24, clk=22)

#原理(principle)
#(0,0)...X
#.
#.
#Y
#((0,0), (0, 1), ...(0, 15))
#0x7f = 0111 1111
# dms.display_buf = (0x7f, 0x08, 0x7f, 0x00, 0x7c, 0x54, 0x5c, 0x00,
                  # 0x7c, 0x40, 0x00,0x7c, 0x40, 0x38, 0x44, 0x38)

# dms.display_buf = [int('01111111', 2), 
                   # int('00001000', 2), 
                   # int('01111111', 2), 
                   # int('00000000', 2), 
                   # int('01111100', 2), 
                   # int('01010100', 2), 
                   # int('01011100', 2), 
                   # int('00000000', 2),
                   # int('01111100', 2), 
                   # int('01000000', 2), 
                   # int('00000000', 2), 
                   # int('01111100', 2), 
                   # int('01000000', 2), 
                   # int('00111000', 2), 
                   # int('01000100', 2), 
                   # int('00111000', 2)]

## 显示'Hello'(display 'Hello')
lst = ['1010000000000000', 
       '1010000000000000',
       '1010111010010010',
       '1110101010010101',
       '1010111010010101',
       '1010100010010101',
       '1010111011011010',
       '0000000000000000']             

dms.set_buf_horizontal(lst)
dms.update_display()

time.sleep(2)
dms.clear()
time.sleep(1)
lst = ['01111111', 
       '00001000', 
       '01111111', 
       '00000000', 
       '01111100', 
       '01010100', 
       '01011100', 
       '00000000',
       '01111100', 
       '01000000', 
       '00000000', 
       '01111100', 
       '01000000', 
       '00111000',
       '01000100', 
       '00111000']             

dms.set_buf_vertical(lst)
dms.update_display()

time.sleep(2)
dms.clear()
