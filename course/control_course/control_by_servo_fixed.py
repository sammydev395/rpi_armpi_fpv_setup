#!/usr/bin/python3
# coding=utf8
# 第8章 ArmPi FPV逆运动学基础及实战应用课程/第3课 单次控制多个舵机(8. ArmPi FPV inverse kinematics basics & application course/Lesson 3 multiple servos control)
import Setup_paths  # This sets up the Python paths for SDK imports
import time
from common.ros_robot_controller_sdk import Board

print("🔧 Initializing ArmPi FPV Servo Control...")

try:
    board = Board()
    print("✅ Board initialized successfully")
    
    print("🎯 Testing servo 1...")
    board.bus_servo_set_position(0.5, [[1, 200]])
    time.sleep(1)
    board.bus_servo_set_position(0.5, [[1, 700]])
    time.sleep(1)
    board.bus_servo_set_position(0.5, [[1, 300]])
    time.sleep(1)

    print("🎯 Testing servos 2 and 3...")
    board.bus_servo_set_position(0.5, [[2, 200], [3, 700]])
    time.sleep(1)
    board.bus_servo_set_position(0.5, [[2, 800], [3, 500]])
    time.sleep(1)
    board.bus_servo_set_position(0.5, [[2, 500], [3, 200]])
    time.sleep(1)

    print("🎯 Testing servo 4...")
    board.bus_servo_set_position(0.5, [[4, 550]])
    time.sleep(1)
    board.bus_servo_set_position(0.5, [[4, 800]])
    time.sleep(1)

    print("🎯 Testing servo 5...")
    board.bus_servo_set_position(0.5, [[5, 800]])
    time.sleep(1)
    board.bus_servo_set_position(0.5, [[5, 500]])
    time.sleep(1)
    board.bus_servo_set_position(0.5, [[5, 650]])
    time.sleep(1)

    print("🎯 Testing servo 6...")
    board.bus_servo_set_position(0.5, [[6, 200]])
    time.sleep(1)
    board.bus_servo_set_position(1, [[6, 800]])
    time.sleep(1)
    board.bus_servo_set_position(0.5, [[6, 500]])
    time.sleep(1)
    
    print("✅ Servo control test completed!")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Check if all SDK modules are properly installed")
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Check hardware connections and servo communication") 