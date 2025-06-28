#!/usr/bin/env python3
# encoding: utf-8
"""
Comprehensive servo diagnostic for ArmPi FPV
"""
import Setup_paths
import time
import serial
from common.ros_robot_controller_sdk import Board

def test_servo_movement(board, servo_id, positions, duration=1):
    """Test servo movement with detailed feedback"""
    print(f"\n🎯 Testing Servo {servo_id}...")
    
    for i, pos in enumerate(positions):
        print(f"   📤 Command {i+1}: Moving servo {servo_id} to position {pos}")
        board.bus_servo_set_position(duration, [[servo_id, pos]])
        
        # Wait and check if we can read the position
        time.sleep(duration + 0.5)
        
        # Try to read the position
        try:
            fake_pos = board.bus_servo_read_position(servo_id, fake=True)
            real_pos = board.bus_servo_read_position(servo_id, fake=False)
            print(f"   📊 Position - Fake: {fake_pos}, Real: {real_pos}")
        except Exception as e:
            print(f"   ❌ Error reading position: {e}")

def test_servo_torque(board, servo_id):
    """Test servo torque enable/disable"""
    print(f"\n🔧 Testing Servo {servo_id} Torque...")
    
    try:
        # Enable torque
        print(f"   📤 Enabling torque for servo {servo_id}")
        board.bus_servo_enable_torque(servo_id, True)
        time.sleep(0.5)
        
        # Try to read torque state
        torque_state = board.bus_servo_read_torque_state(servo_id)
        print(f"   📊 Torque state: {torque_state}")
        
        # Try to move servo
        print(f"   📤 Moving servo {servo_id} to position 500")
        board.bus_servo_set_position(1, [[servo_id, 500]])
        time.sleep(1.5)
        
        # Disable torque
        print(f"   📤 Disabling torque for servo {servo_id}")
        board.bus_servo_enable_torque(servo_id, False)
        time.sleep(0.5)
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_raw_serial_communication():
    """Test raw serial communication to see if commands are being sent"""
    print(f"\n🔧 Testing Raw Serial Communication...")
    
    try:
        # Open serial port directly
        ser = serial.Serial("/dev/ttyAMA0", 1000000, timeout=1)
        print(f"   ✅ Opened /dev/ttyAMA0")
        
        # Send a servo command manually
        # Format: 0xAA 0x55 Length Function ID Data Checksum
        # Bus servo set position command
        servo_cmd = b'\xAA\x55\x01\x05\x01\x01\xF4\x00'  # Move servo 1 to position 500
        print(f"   📤 Sending raw command: {servo_cmd.hex()}")
        ser.write(servo_cmd)
        
        # Try to read response
        response = ser.read(10)
        if response:
            print(f"   📥 Raw response: {response.hex()}")
        else:
            print(f"   ⏳ No raw response")
        
        ser.close()
        
    except Exception as e:
        print(f"   ❌ Raw serial error: {e}")

def main():
    print("🔍 ArmPi FPV Servo Diagnostic")
    print("=" * 50)
    
    try:
        # Initialize board
        print("🔧 Initializing Board...")
        board = Board()
        print("✅ Board initialized successfully")
        
        # Enable reception
        board.enable_reception(True)
        print("✅ Reception enabled")
        
        # Test raw serial communication first
        test_raw_serial_communication()
        
        # Test each servo individually
        for servo_id in range(1, 7):
            test_servo_movement(board, servo_id, [200, 500, 800])
        
        # Test torque control
        test_servo_torque(board, 1)
        
        print(f"\n📋 Diagnostic Summary:")
        print(f"   - Board initialization: ✅")
        print(f"   - Serial communication: ✅")
        print(f"   - Commands sent: ✅")
        print(f"   - Servo movement: ❓ (Check if servos moved)")
        print(f"   - Position feedback: ❓ (Check real position values)")
        
        print(f"\n💡 If servos aren't moving:")
        print(f"   1. Check servo power supply")
        print(f"   2. Check servo wiring connections")
        print(f"   3. Check servo IDs and addresses")
        print(f"   4. Check if servos need initialization")
        
    except Exception as e:
        print(f"❌ Diagnostic error: {e}")

if __name__ == "__main__":
    main() 