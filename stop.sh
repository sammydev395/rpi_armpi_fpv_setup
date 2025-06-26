#!/bin/bash

echo "🛑 Stopping ArmPi FPV Container..."

# Stop the container
docker-compose down

# Disable X11 forwarding for security
xhost -local:root

echo "✅ Container stopped!"
echo ""
echo "📋 Container Status:"
docker ps -a --filter name=armpi_fpv --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
