#!/usr/bin/env python3
# encoding: utf-8
"""
Test different UART configurations for ArmPi FPV
"""
import Setup_paths
import time
import serial
import subprocess
import os

def check_uart_enabled():
    """Check which UART interfaces are enabled"""
    print("🔍 Checking UART Configuration...")
    
    # Check config.txt for UART settings
    try:
        with open('/boot/config.txt', 'r') as f:
            config = f.read()
            print("📋 /boot/config.txt UART settings:")
            for line in config.split('\n'):
                if 'uart' in line.lower() or 'serial' in line.lower():
                    print(f"   {line.strip()}")
    except Exception as e:
        print(f"   ❌ Could not read /boot/config.txt: {e}")
    
    # Check available serial devices
    print(f"\n📱 Available serial devices:")
    devices = ['/dev/ttyAMA10', '/dev/ttyS0', '/dev/ttyAMA0', '/dev/ttyAMA1']
    for device in devices:
        if os.path.exists(device):
            print(f"   ✅ {device}")
        else:
            print(f"   ❌ {device} (not found)")

def test_uart_interface(device_name, baudrate=1000000):
    """Test a specific UART interface"""
    print(f"\n🔧 Testing {device_name} at {baudrate} baud...")
    
    try:
        # Try to open the port
        ser = serial.Serial(device_name, baudrate, timeout=1)
        print(f"   ✅ Successfully opened {device_name}")
        
        # Send a test command (Hiwonder protocol header)
        test_cmd = b'\xAA\x55\x01\x05\x01\x00'  # Example bus servo read command
        print(f"   📤 Sending test command: {test_cmd.hex()}")
        ser.write(test_cmd)
        
        # Try to read response
        response = ser.read(10)
        if response:
            print(f"   📥 Response received: {response.hex()}")
            return True
        else:
            print(f"   ⏳ No response (timeout)")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    finally:
        try:
            ser.close()
        except:
            pass

def enable_uart_interfaces():
    """Show how to enable additional UART interfaces"""
    print(f"\n🔧 To enable additional UART interfaces, add to /boot/config.txt:")
    print(f"   # Enable UART0")
    print(f"   enable_uart=1")
    print(f"   dtoverlay=uart0")
    print(f"   ")
    print(f"   # Enable UART1")
    print(f"   dtoverlay=uart1")
    print(f"   ")
    print(f"   # Enable UART2")
    print(f"   dtoverlay=uart2")
    print(f"   ")
    print(f"   # Enable UART3")
    print(f"   dtoverlay=uart3")
    print(f"   ")
    print(f"   # Enable UART4")
    print(f"   dtoverlay=uart4")
    print(f"   ")
    print(f"   # Enable UART5")
    print(f"   dtoverlay=uart5")

def main():
    print("🔍 ArmPi FPV UART Configuration Test")
    print("=" * 50)
    
    # Check current UART configuration
    check_uart_enabled()
    
    # Test available interfaces
    print(f"\n🧪 Testing UART Interfaces...")
    
    # Test the current interface
    test_uart_interface("/dev/ttyAMA10")
    
    # Show how to enable more interfaces
    enable_uart_interfaces()
    
    print(f"\n📋 Summary:")
    print(f"   - Current interface: /dev/ttyAMA10 (working but no hardware response)")
    print(f"   - Need vendor to specify which UART interface ArmPi should use")
    print(f"   - May need to enable additional UART interfaces in /boot/config.txt")
    print(f"   - Hardware connection diagram required from vendor")

if __name__ == "__main__":
    main() 