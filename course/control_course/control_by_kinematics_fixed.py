#!/usr/bin/env python3
# encoding: utf-8
# 第8章 ArmPi FPV逆运动学基础及实战应用课程/第4课 机械臂上下左右移动(8. ArmPi FPV inverse kinematics basics & application/Lesson 4 movement control)
import Setup_paths  # This sets up the Python paths for SDK imports
import time
import numpy as np
from kinematics import transform
from common.ros_robot_controller_sdk import Board
from kinematics.kinematics_controller import KinematicsController

print("🔧 Initializing ArmPi FPV Kinematics Control...")

try:
    board = Board()
    print("✅ Board initialized successfully")
    
    controller = KinematicsController(board)
    print("✅ Kinematics controller initialized successfully")
    
    ###########inverse_kinematics##################
    # [x, y, z(m)], pitch, [pitch_min, pitch_max](deg)获取运动学逆解([x, y, z(m)], pitch, [pitch_min, pitch_max](deg) get inverse kinematics solution)
    # res = controller.get_all_ik([0, 0.1, 0.1], 0, [-180, 180])
    print('ik input: \nxyz(m): {}\npitch(deg): {}\npitch_range(deg): {}\n'.format([0.2, 0, 0.25], 0, [-180, 180]))
    
    res = controller.set_pose_target([0.2, 0, 0.25], 0, [-180, 180], roll=90)
    print('ik output: \nik pulse: {}\ncurrent pulse: {}\nrpy{}\n'.format(*res[1:-1]))
    
    if res[1]:
        print("🎯 Setting servo positions...")
        board.bus_servo_set_position(1, [[2, res[1][4]], [3, res[1][3]], [4, res[1][2]], [5, res[1][1]], [6, res[1][0]]])
        time.sleep(1)
        
        res = controller.set_joint_value_target(*res[1])
        print('fk output:\nxyz(m): {}\nqua: {}'.format(*res[2]))
        print('rpy:', transform.qua2rpy(res[-1][-1]))
        
        print("🔄 Starting movement loop...")
        while True:
            for i in np.arange(0.25, 0.14, -0.01):
                controller.go_pose_target([0.18, 0, i], 0, [-180, 180], roll=np.interp(i, [0.15, 0.25], [-90, 90]), use_time=0.1)
                time.sleep(0.1)
            for i in np.arange(0.15, 0.26, 0.01):
                controller.go_pose_target([0.18, 0, i], 0, [-180, 180], roll=np.interp(i, [0.15, 0.25], [-90, 90]), use_time=0.1)
                time.sleep(0.1)
    else:
        print("❌ Failed to get inverse kinematics solution")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Check if all SDK modules are properly installed")
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Check hardware connections and servo communication") 