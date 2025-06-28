#!/usr/bin/env python3
# encoding: utf-8
"""
Common classes for kinematics module
"""

class Pose:
    """Simple Pose class for kinematics calculations"""
    def __init__(self, position=None, orientation=None):
        self.position = position or [0, 0, 0]
        self.orientation = orientation or [0, 0, 0, 1]  # quaternion [x, y, z, w]
    
    def __repr__(self):
        return f"Pose(position={self.position}, orientation={self.orientation})" 