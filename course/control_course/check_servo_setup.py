#!/usr/bin/env python3
# encoding: utf-8
"""
Check servo status and communication on ArmPi FPV
"""
import Setup_paths  # This sets up the Python paths for SDK imports

import time
from common.ros_robot_controller_sdk import Board

def check_servo_status():
    print("Checking ArmPi FPV servo status...")
    board = Board()
    
    # Enable reception for feedback
    print("Enabling reception...")
    board.enable_reception(True)
    time.sleep(0.5)
    
    # Check each servo
    for servo_id in range(1, 7):
        try:
            print(f"\nServo {servo_id}:")
            
            # Read current position (fake=True uses internal dictionary)
            position = board.bus_servo_read_position(servo_id, fake=True)
            print(f"  Position (fake): {position}")
            
            # Try real read
            real_position = board.bus_servo_read_position(servo_id, fake=False)
            print(f"  Position (real): {real_position}")
            
            # Read torque state
            torque = board.bus_servo_read_torque_state(servo_id)
            print(f"  Torque enabled: {torque}")
            
            # Read voltage
            voltage = board.bus_servo_read_vin(servo_id)
            print(f"  Voltage: {voltage}")
            
            # Read temperature
            temp = board.bus_servo_read_temp(servo_id)
            print(f"  Temperature: {temp}")
            
        except Exception as e:
            print(f"  Error reading servo {servo_id}: {e}")
    
    print("\nServo status check completed!")

if __name__ == "__main__":
    try:
        check_servo_status()
    except KeyboardInterrupt:
        print("\nCheck interrupted by user")
    except Exception as e:
        print(f"Error during check: {e}") 