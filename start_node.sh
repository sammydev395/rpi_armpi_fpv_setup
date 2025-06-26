#!/bin/bash
echo "Starting ArmPi FPV ROS Node..."

# Source ROS environment
source /opt/ros/noetic/setup.bash
source /home/ubuntu/armpi_fpv/devel/setup.bash

# Set ROS environment variables for Docker container
export ROS_MASTER_URI=http://localhost:11311
export ROS_HOSTNAME=localhost
export ROS_IP=localhost

# Change to workspace directory
cd /home/ubuntu/armpi_fpv

echo "ROS Environment:"
echo "ROS_MASTER_URI: $ROS_MASTER_URI"
echo "ROS_HOSTNAME: $ROS_HOSTNAME"
echo ""

echo "Available launch files:"
echo "1. armpi_fpv_bringup bringup.launch - Main robot bringup"
echo "2. armpi_fpv_bringup usb_cam.launch - Camera only"
echo "3. armpi_fpv_moveit_config demo.launch - MoveIt demo"
echo ""

# Launch the main bringup file
echo "Launching ArmPi FPV bringup..."
roslaunch armpi_fpv_bringup bringup.launch
