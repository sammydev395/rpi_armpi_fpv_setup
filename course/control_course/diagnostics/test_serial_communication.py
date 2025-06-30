#!/usr/bin/env python3
# encoding: utf-8
"""
Test serial communication for ArmPi FPV
"""
import Setup_paths
import time
import serial

def test_serial_port(port_name, baudrate=1000000):
    """Test if we can open and communicate with a serial port"""
    print(f"\nTesting {port_name} at {baudrate} baud...")
    try:
        # Try to open the port
        ser = serial.Serial(port_name, baudrate, timeout=1)
        print(f"  ✅ Successfully opened {port_name}")
        
        # Try to read some data
        print(f"  📡 Attempting to read data...")
        data = ser.read(10)
        if data:
            print(f"  📥 Received data: {data.hex()}")
        else:
            print(f"  ⏳ No data received (timeout)")
        
        # Try to write some test data
        test_data = b'\xAA\x55\x01\x00\x00\x00'
        print(f"  📤 Sending test data: {test_data.hex()}")
        ser.write(test_data)
        
        # Try to read response
        response = ser.read(10)
        if response:
            print(f"  📥 Response: {response.hex()}")
        else:
            print(f"  ⏳ No response received")
        
        ser.close()
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    print("🔍 Testing ArmPi FPV Serial Communication")
    print("=" * 50)
    
    # Test the expected port
    test_serial_port("/dev/ttyAMA10")
    
    # Test other common ports
    common_ports = [
        "/dev/ttyAMA0",
        "/dev/ttyAMA1", 
        "/dev/ttyS0",
        "/dev/ttyS1",
        "/dev/ttyUSB0",
        "/dev/ttyUSB1"
    ]
    
    print(f"\n🔍 Testing other common serial ports...")
    for port in common_ports:
        try:
            test_serial_port(port)
        except:
            pass
    
    print(f"\n✅ Serial communication test completed!")

if __name__ == "__main__":
    main() 