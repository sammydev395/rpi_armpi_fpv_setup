#!/bin/bash

echo "🔄 Starting ArmPi FPV Container..."

# Enable X11 forwarding
xhost +local:root

# Start the container
docker-compose up -d

echo "✅ Container started!"
echo ""
echo "📋 Container Status:"
docker ps --filter name=armpi_fpv --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "🎯 To enter the container:"
echo "   ./enter.sh"
echo ""
echo "🤖 To start ROS directly:"
echo "   ./start_ros.sh"
