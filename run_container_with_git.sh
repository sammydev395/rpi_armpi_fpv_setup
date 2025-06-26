#!/bin/bash

# Stop and remove existing container if it exists
docker stop armpi-ssh-hardware 2>/dev/null || true
docker rm armpi-ssh-hardware 2>/dev/null || true

# Run the container with SSH keys and config mounted, using the same name Cursor expects
docker run -d \
    --name armpi-ssh-hardware \
    --privileged \
    -p 2222:22 \
    -p 8080:8080 \
    --device=/dev/video0:/dev/video0 \
    -v ~/.ssh/id_ed25519_armpi_container:/home/ubuntu/.ssh/id_ed25519:ro \
    -v ~/.ssh/id_ed25519_armpi_container.pub:/home/ubuntu/.ssh/id_ed25519.pub:ro \
    -v ~/.ssh/config:/home/ubuntu/.ssh/config:ro \
    armpi_fpv_ros \
    bash -c "while true; do sleep 30; done"

echo "Container started with Git support. Cursor IDE can now connect to port 2222."
