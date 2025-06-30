#!/usr/bin/env python3
# encoding: utf-8
"""
Test different communication methods with ArmPi board
"""
import Setup_paths
import time
import serial
import os

def test_uart_with_different_baudrates(device_name):
    """Test UART with different baud rates"""
    print(f"\n🔧 Testing {device_name} with different baud rates...")
    
    baudrates = [9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600, 1000000]
    
    for baudrate in baudrates:
        try:
            ser = serial.Serial(device_name, baudrate, timeout=0.5)
            print(f"   📡 Testing {baudrate} baud...")
            
            # Send a simple test command
            test_cmd = b'\xAA\x55\x01\x05\x01\x00'
            ser.write(test_cmd)
            
            # Try to read response
            response = ser.read(10)
            if response:
                print(f"   📥 Response at {baudrate} baud: {response.hex()}")
                ser.close()
                return True
            else:
                print(f"   ⏳ No response at {baudrate} baud")
            
            ser.close()
        except Exception as e:
            print(f"   ❌ Error at {baudrate} baud: {e}")
    
    return False

def test_simple_commands(device_name):
    """Test simple commands that might work"""
    print(f"\n🔧 Testing simple commands on {device_name}...")
    
    try:
        ser = serial.Serial(device_name, 1000000, timeout=1)
        
        # Test different simple commands
        commands = [
            b'\xAA\x55\x01\x00\x00\x00',  # System command
            b'\xAA\x55\x01\x01\x00\x00',  # LED command
            b'\xAA\x55\x01\x02\x00\x00',  # Buzzer command
            b'\xAA\x55\x01\x03\x00\x00',  # Motor command
            b'\xAA\x55\x01\x04\x00\x00',  # PWM servo command
            b'\xAA\x55\x01\x05\x00\x00',  # Bus servo command
            b'\xAA\x55\x01\x06\x00\x00',  # Key command
            b'\xAA\x55\x01\x07\x00\x00',  # IMU command
        ]
        
        for i, cmd in enumerate(commands):
            print(f"   📤 Command {i+1}: {cmd.hex()}")
            ser.write(cmd)
            
            response = ser.read(10)
            if response:
                print(f"   📥 Response: {response.hex()}")
                ser.close()
                return True
            else:
                print(f"   ⏳ No response")
        
        ser.close()
        return False
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("🔍 Comprehensive ArmPi Board Communication Test")
    print("=" * 60)
    
    # Test primary UART interface
    primary_uart = "/dev/ttyAMA0"
    
    if os.path.exists(primary_uart):
        print(f"✅ Testing primary UART: {primary_uart}")
        
        # Test with different baud rates
        if test_uart_with_different_baudrates(primary_uart):
            print(f"🎉 Found working baud rate!")
            return
        
        # Test simple commands
        if test_simple_commands(primary_uart):
            print(f"🎉 Found working command!")
            return
        
        print(f"❌ No response from {primary_uart}")
    else:
        print(f"❌ Primary UART {primary_uart} not found")
    
    print(f"\n📋 Summary:")
    print(f"   - ArmPi board is connected and powered (LEDs lit)")
    print(f"   - No UART communication is working")
    print(f"   - Board might use different communication method")
    print(f"   - Check vendor documentation for correct interface")

if __name__ == "__main__":
    main() 