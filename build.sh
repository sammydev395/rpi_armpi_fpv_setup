#!/bin/bash

echo "🏗️  Building ArmPi FPV Docker Container..."

# Enable X11 forwarding for GUI applications
xhost +local:root

# Build the Docker container
docker-compose build

echo "✅ Build complete!"
echo ""
echo "🚀 Next steps:"
echo "   ./start.sh    - Start the container"
echo "   ./enter.sh    - Enter the container shell"
echo "   ./start_ros.sh - Start ROS directly"
echo "   ./stop.sh     - Stop the container"
