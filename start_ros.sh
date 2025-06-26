#!/bin/bash

# Check if container is running
if ! docker ps --filter name=armpi_fpv --filter status=running -q | grep -q .; then
    echo "❌ Container is not running. Starting container first..."
    ./start.sh
    echo "⏳ Waiting for container to be ready..."
    sleep 3
fi

echo "🤖 Starting ROS in ArmPi FPV Container..."
echo "This will launch ROS with the startup scripts..."
echo ""

# Execute the ROS startup script inside the container
docker exec -it armpi_fpv /bin/zsh -c "source ~/.zshrc && source /opt/ros/noetic/setup.zsh && source ~/armpi_fpv/devel/setup.zsh && roscore"
