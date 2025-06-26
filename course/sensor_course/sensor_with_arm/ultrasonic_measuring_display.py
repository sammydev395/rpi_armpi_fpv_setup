#!/usr/bin/env python3
# encoding:utf-8
# 第15章 拓展课程之传感器开发与应用\2.拓展课程-传感器应用开发课程\第2课 机械臂超声波扫描显示(15. expanded course of sensor development and application\1. sensor basic application course\Lesson 2 ultrasonic scanning display)
import time
import math
import signal
import numpy as np
import matplotlib.pyplot as plt
from sensor import ultrasonic_sensor
from common.ros_robot_controller_sdk import Board
from kinematics.kinematics_controller import KinematicsController

board = Board()
controller = KinematicsController(board)
board.bus_servo_set_position(0.5, [[1, 200]])
controller.go_pose_target([0.1, 0, 0.1], 30, [-90, 90], 0, 1)

s = ultrasonic_sensor.Ultrasonic()
s.setBreathCycle(0, 0, 2000)
s.setBreathCycle(1, 0, 2000)  # 设置超声波RGB颜色渐变模式(set ultrasonic RGB color gradient mode)
time.sleep(3)  

start = True
#关闭前处理(process before closing)
def Stop(signum, frame):
    global start

    start = False
    print('关闭中...')

signal.signal(signal.SIGINT, Stop)

turning_radius = 0.25

#旋转半径R(rotation radius R)
# 计算出在旋转半径为R、角度a时的坐标(calculate the coordinate when the rotation radius is R, angle is a)
def get_point(a, r=turning_radius):
    x = math.sin(math.radians(a))*r
    y = math.cos(math.radians(a))*r
    return x, y

ax = []                    # 定义一个 x 轴的空列表用来接收动态的数据(define an empty list for the x-axis to receive dynamic data)
ay = []                    # 定义一个 y 轴的空列表用来接收动态的数据(define an empty list for the y-axis to receive dynamic data)
#传感器最大接收数值，距离大于600mm时超声波传感器易被干扰(the sensor's maximum receiving value. Ultrasonic sensors are prone to interference when the distance is greater than 600mm)
maximum_range = 50
plt.ion()                  # 开启一个画图的窗口(open a plotting window)
plt.xlim(-maximum_range, maximum_range)
plt.ylim(0, maximum_range)
plt.grid(True)

def two_dimensional_scatter_diagram():
    global start
    # 扫描角度(scanning angle)
    scan_angle = 180
    # 高度(height)
    z = 0.13
    # 步长越大越块相应的数据也越少(the larger the faster the step size, the fewer corresponding data points)
    step = 2#
    #机械臂运动速度 由于实时画图需要一定时间导致此值过小也不会太快而且会有卡顿感(the robotic arm's movement speed, due to the real-time plotting requiring a certain amount of time, means that even if this value is too small, it won't be too fast, and there may still be a sense of lag)
    use_time = 0.05

    x, y = get_point(0) 
    controller.go_pose_target([x, y, z], -5, [-90, 90], 0, 2)
    time.sleep(2.2)
    
    data = np.zeros(scan_angle + 1, dtype=np.int)

    start_value = 0
    end_value = scan_angle + 1
    last_start_value = 0
    begin_time = time.time()
    end_time = 0
    while start:
        for j in range(start_value, end_value, step):                       #控制探测角度(control detection angle)
            x, y = get_point(j)
            end_time = time.time()
            run_time = end_time - begin_time
            if use_time > run_time:
                time.sleep(abs(use_time - run_time)*0.9)
            controller.go_pose_target([x, y, z], -5, [-90, 90], 0, use_time)
            begin_time = time.time()
            data[j] = s.getDistance() / 10
            if data[j] > maximum_range: 
                data[j] = maximum_range
            y = data[j]*math.sin(math.radians(180 - j))
            x = data[j]*math.cos(math.radians(180 - j))
            ax.append(x)                                                 # 添加 i 到 x 轴的数据中(add i to x-axis data)
            ay.append(y)                                                # 添加 i 的平方到 y 轴的数据中(add the square of i to the y-axis data)
            plt.xlim(-maximum_range, maximum_range)
            plt.ylim(0, maximum_range)
            plt.grid(True)
            plt.plot(ax[-2:], ay[-2:])
            plt.pause(0.000001)  # 暂停一下(pause for a moment)
            last_start_value = j
            if not start:
                break
        end_value = start_value - 1 
        start_value = last_start_value 
        step = -step
        plt.clf()
        ax.clear()
        ay.clear()

if __name__ == "__main__":
    two_dimensional_scatter_diagram()
