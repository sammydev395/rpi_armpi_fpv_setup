#!/usr/bin/env python3
# encoding: utf-8
import time
import numpy as np
from kinematics import transform
from common.ros_robot_controller_sdk import Board
from kinematics.kinematics_controller import KinematicsController

board = Board()
controller = KinematicsController(board)

###########forward_kinematics##################
print('当前各连杆长度(m): \nbase_link: {}\nlink1: {}\nlink2: {}\nlink3: {}\ntool_link: {}\n'.format(*controller.get_link()[-1]))  # 详细说明请参考transform里的注释
print('当期各关节范围(deg): \njoint1: {}\njoint2: {}\njoint3: {}\njoint4: {}\njoint5: {}\n'.format(*controller.get_joint_range()[-1]))  #以角度为单位返回
print('fk input: {}'.format([500, 500, 500, 500, 500]))
res = controller.set_joint_value_target(500, 500, 500, 500, 500)  #获取运动学正解
print('fk output:\nxyz(m): {}\nqua: {}'.format(*res[2]))
print('rpy:', transform.qua2rpy(res[-1][-1]))
board.bus_servo_set_position(1, [[2, 500], [3, 500], [4, 500], [5, 500], [6, 500]])
time.sleep(1)

print('----------------------------------------------------------------------------------------------------------------')
###########inverse_kinematics##################
# [x, y, z(m)], pitch, [pitch_min, pitch_max](deg)获取运动学逆解
# res = controller.get_all_ik([0, 0.1, 0.1], 0, [-180, 180])
print('ik input: \nxyz(m): {}\npitch(deg): {}\npitch_range(deg): {}\n'.format([0.2, 0, 0.25], 0, [-180, 180]))
res = controller.set_pose_target([0.2, 0, 0.25], 0, [-180, 180], roll=90)
print('ik output: \nik pulse: {}\ncurrent pulse: {}\nrpy{}\n'.format(*res[1:-1]))
if res[1]:
    board.bus_servo_set_position(1, [[2, res[1][4]], [3, res[1][3]], [4, res[1][2]], [5, res[1][1]], [6, res[1][0]]])
time.sleep(1)
res = controller.set_joint_value_target(*res[1])
print('fk output:\nxyz(m): {}\nqua: {}'.format(*res[2]))
print('rpy:', transform.qua2rpy(res[-1][-1]))
for i in np.arange(0.25, 0.14, -0.01):
    controller.go_pose_target([0.18, 0, i], 0, [-180, 180], roll=np.interp(i, [0.15, 0.25], [-90, 90]), use_time=0.1)
    time.sleep(0.1)
for i in np.arange(0.15, 0.26, 0.01):
    controller.go_pose_target([0.18, 0, i], 0, [-180, 180], roll=np.interp(i, [0.15, 0.25], [-90, 90]), use_time=0.1)
    time.sleep(0.1)
print('----------------------------------------------------------------------------------------------------------------')
# 设置连杆长度(m)base_link, link1, link2, link3, tool_link
controller.set_link(0.065, 0.1, 0.095, 0.05, 0.1)

# 设置关节范围(deg)joint1, joint2, joint3, joint4, joint5
controller.set_joint_range([-90, 0], [-90, 0], [-90, 0], [-90, 0], [-90, 0])  
print('当前各连杆长度(m): \nbase_link: {}\nlink1: {}\nlink2: {}\nlink3: {}\ntool_link: {}\n'.format(*controller.get_link()[-1]))  # 详细说明请参考transform里的注释
print('当期各关节范围(deg): \njoint1: {}\njoint2: {}\njoint3: {}\njoint4: {}\njoint5: {}\n'.format(*controller.get_joint_range()[-1]))  #以角度为单位返回

