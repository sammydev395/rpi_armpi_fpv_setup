#!/bin/bash

# ArmPi FPV Docker Container Runner with Hardware Access
# This script runs the ArmPi container with proper device mapping

echo "🚀 Starting ArmPi FPV Container with Hardware Access..."

# Stop and remove existing container if running
echo "🧹 Cleaning up existing container..."
docker stop armpi-ssh-hardware 2>/dev/null || true
docker rm armpi-ssh-hardware 2>/dev/null || true

# Check if image exists, build if not
if ! docker images | grep -q "armpi-fpv-complete"; then
    echo "🔨 Building ArmPi FPV Docker image..."
    docker build -f Dockerfile.complete -t armpi-fpv-complete .
fi

# Run container with comprehensive device access
echo "🐳 Starting Docker container..."
docker run -d \
  --name armpi-ssh-hardware \
  --restart unless-stopped \
  -p 2222:22 \
  -p 8080:8080 \
  -p 9090:9090 \
  -p 11311:11311 \
  --device=/dev/video0:/dev/video0 \
  --device=/dev/video1:/dev/video1 \
  --device=/dev/ttyAMA10:/dev/ttyAMA10 \
  --privileged \
  -v /dev:/dev \
  -v /sys:/sys \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  armpi-fpv-complete

# Wait a moment for container to start
sleep 5

# Check container status
if docker ps | grep -q armpi-ssh-hardware; then
    echo ""
    echo "✅ ArmPi FPV Container Started Successfully!"
    echo ""
    echo "📡 Connection Information:"
    echo "   SSH Access:      ssh ubuntu@localhost -p 2222"
    echo "   SSH (Remote):    ssh ubuntu@$(hostname) -p 2222"
    echo "   Web Video:       http://localhost:8080"
    echo "   ROS Bridge:      ws://localhost:9090"
    echo "   ROS Master:      http://localhost:11311"
    echo ""
    echo "🔐 SSH Authentication:"
    echo "   Username:        ubuntu"
    echo "   Password:        ubuntu"
    echo "   SSH Key:         Pre-configured for sammy_o@win11"
    echo ""
    echo "🔍 Hardware Status:"
    docker exec armpi-ssh-hardware ls -la /dev/video* 2>/dev/null | head -3 || echo "   ⚠️  No video devices found"
    docker exec armpi-ssh-hardware ls -la /dev/ttyAMA10 2>/dev/null || echo "   ⚠️  No serial device ttyAMA10 found"
    echo ""
    echo "🚀 Quick Commands:"
    echo "   Start ROS:       docker exec armpi-ssh-hardware /home/ubuntu/start_node.sh"
    echo "   Shell Access:    docker exec -it armpi-ssh-hardware /bin/zsh"
    echo "   Stop Container:  docker stop armpi-ssh-hardware"
    echo ""
    echo "🎯 Ready for development with Cursor IDE!"
else
    echo "❌ Failed to start container"
    echo "📋 Container logs:"
    docker logs armpi-ssh-hardware 2>&1 | tail -20
fi
