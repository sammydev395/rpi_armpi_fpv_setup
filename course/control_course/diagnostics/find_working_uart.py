#!/usr/bin/env python3
# encoding: utf-8
"""
Find which UART interface the ArmPi board is connected to
"""
import Setup_paths
import time
import serial
import os

def test_uart_interface(device_name, baudrate=1000000):
    """Test a specific UART interface with Hiwonder protocol"""
    print(f"\n🔧 Testing {device_name}...")
    
    try:
        # Try to open the port
        ser = serial.Serial(device_name, baudrate, timeout=1)
        print(f"   ✅ Opened {device_name}")
        
        # Send Hiwonder protocol command (bus servo read position for servo 1)
        test_cmd = b'\xAA\x55\x01\x05\x01\x00'  # Read servo 1 position
        print(f"   📤 Sending: {test_cmd.hex()}")
        ser.write(test_cmd)
        
        # Try to read response
        response = ser.read(10)
        if response:
            print(f"   📥 Response: {response.hex()}")
            print(f"   🎉 SUCCESS! {device_name} is working!")
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
    print("🔍 Finding Working UART Interface for ArmPi FPV")
    print("=" * 50)
    
    # Test all available UART interfaces
    uart_interfaces = [
        "/dev/ttyAMA0",   # Primary UART (most likely)
        "/dev/ttyAMA1",   # Secondary UART
        "/dev/ttyAMA2",   # Additional UART
        "/dev/ttyAMA3",   # Additional UART
        "/dev/ttyAMA4",   # Additional UART
        "/dev/ttyAMA10",  # Current setting
    ]
    
    print(f"📱 Available UART devices:")
    for device in uart_interfaces:
        if os.path.exists(device):
            print(f"   ✅ {device}")
        else:
            print(f"   ❌ {device} (not found)")
    
    print(f"\n🧪 Testing each UART interface...")
    
    working_interface = None
    for device in uart_interfaces:
        if os.path.exists(device):
            if test_uart_interface(device):
                working_interface = device
                break
    
    print(f"\n📋 Results:")
    if working_interface:
        print(f"   🎉 Working interface: {working_interface}")
        print(f"   💡 Update SDK to use: device='{working_interface}'")
    else:
        print(f"   ❌ No UART interface responded")
        print(f"   💡 Check hardware connections")

if __name__ == "__main__":
    main() 