#!/bin/bash

# Check if container is running
if ! docker ps --filter name=armpi_fpv --filter status=running -q | grep -q .; then
    echo "❌ Container is not running. Starting container first..."
    ./start.sh
    echo "⏳ Waiting for container to be ready..."
    sleep 3
fi

echo "🚪 Entering ArmPi FPV Container..."
docker exec -it armpi_fpv /bin/zsh
