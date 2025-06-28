#!/bin/bash

# ArmPi FPV Docker Container Runner with Hardware Access
# This script runs the ArmPi container with proper device mapping using snapshot image

echo "🚀 Starting ArmPi FPV Container with Hardware Access..."

# Stop and remove existing container if running
echo "🧹 Cleaning up existing container..."
docker stop armpi-ssh-hardware 2>/dev/null || true
docker rm armpi-ssh-hardware 2>/dev/null || true

# Use the latest snapshot image with AprilTag and MediaPipe
IMAGE_NAME="armpi_ros_container:with-apriltag-mediapipe"

# Check if snapshot image exists
if ! docker images | grep -q "armpi_ros_container.*with-apriltag-mediapipe"; then
    echo "❌ Snapshot image not found: $IMAGE_NAME"
    echo "Available images:"
    docker images | grep armpi
    exit 1
fi

# Run container with comprehensive device access and SSH keys mounted
echo "🐳 Starting Docker container with snapshot image..."
docker run -d \
  --name armpi-ssh-hardware \
  --restart unless-stopped \
  -p 2222:22 \
  -p 8080:8080 \
  -p 9090:9090 \
  -p 11311:11311 \
  --device=/dev/video0:/dev/video0 \
  --device=/dev/video1:/dev/video1 \
  --device=/dev/ttyAMA0:/dev/ttyAMA0 \
  --privileged \
  -v /dev:/dev \
  -v /sys:/sys \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v /home/sammydev295/.ssh:/home/ubuntu/.ssh_host:ro \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  $IMAGE_NAME

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
    docker exec armpi-ssh-hardware ls -la /dev/ttyAMA0 2>/dev/null || echo "   ⚠️  No serial device ttyAMA0 found"
    echo ""
    echo "📦 Using Snapshot Image: $IMAGE_NAME"
    echo "   - Includes AprilTag v3.x from source"
    echo "   - Includes MediaPipe"
    echo "   - Includes all ROS packages"
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
