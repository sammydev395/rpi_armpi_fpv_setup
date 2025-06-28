#!/usr/bin/env python3
# encoding: utf-8
"""
Python path setup utility for ArmPi FPV course files.
Import this file at the top of any course script to set up the correct Python paths.
"""

import sys
import os

def setup_sdk_paths():
    """Add SDK directories to Python path"""
    # Get the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    
    # Define SDK paths
    armpi_sdk_dir = os.path.join(parent_dir, 'armpi_fpv_sdk')
    common_sdk_dir = os.path.join(armpi_sdk_dir, 'common_sdk')
    kinematics_sdk_dir = os.path.join(armpi_sdk_dir, 'kinematics_sdk')
    sensor_sdk_dir = os.path.join(armpi_sdk_dir, 'sensor_sdk')
    
    # Add to Python path if they exist
    paths_to_add = []
    if os.path.exists(common_sdk_dir):
        paths_to_add.append(common_sdk_dir)
    if os.path.exists(kinematics_sdk_dir):
        paths_to_add.append(kinematics_sdk_dir)
    if os.path.exists(sensor_sdk_dir):
        paths_to_add.append(sensor_sdk_dir)
    
    # Insert at the beginning of sys.path
    for path in reversed(paths_to_add):
        if path not in sys.path:
            sys.path.insert(0, path)
    
    return paths_to_add

# Auto-setup when imported
if __name__ != "__main__":
    setup_sdk_paths() 