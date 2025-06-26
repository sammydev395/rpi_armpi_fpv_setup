# ArmPi FPV Docker Environment

A complete Docker-based development environment for the ArmPi FPV robotic arm with ROS Noetic, SSH access, and hardware integration.

## 🚀 Features

- **Complete ROS Noetic Environment** with MoveIt, Industrial Core, and robotics packages
- **SSH Access** with key-based authentication for remote development
- **Hardware Integration** with USB camera and serial device mapping
- **Web Interfaces** for camera streaming and ROS bridge
- **Development Tools** including Python packages for robotics and computer vision
- **Ready-to-use Scripts** for easy container management

## 📋 Prerequisites

- Docker installed on your system
- ArmPi FPV hardware (optional for development)
- Windows 11 machine with SSH client (for remote development)

## 🛠️ Quick Start

### 1. Build the Docker Image

```bash
docker build -f Dockerfile.complete -t armpi-fpv-complete .
```

### 2. Run with Hardware Access (Recommended)

Use the provided script for full hardware integration:

```bash
./run_armpi_container.sh
```

Or manually run with device mapping:

```bash
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
  armpi-fpv-complete
```

### 3. Connect via SSH

From Windows 11 or any SSH client:

```bash
ssh ubuntu@localhost -p 2222
```

Or connect directly using your machine's IP:

```bash
ssh ubuntu@raspberrypidev -p 2222
```

## 🔧 Container Details

### SSH Access
- **Port:** 2222 (mapped from container port 22)
- **Username:** `ubuntu`
- **Password:** `ubuntu` (fallback)
- **SSH Key:** Pre-configured for `sammy_o@win11`

### Available Services
| Service | Port | Description |
|---------|------|-------------|
| SSH | 2222 | Remote terminal access |
| Web Video Server | 8080 | Camera streaming interface |
| ROS Bridge WebSocket | 9090 | Web-based ROS communication |
| ROS Master | 11311 | ROS core service |

### Hardware Mapping
- **Camera:** `/dev/video0`, `/dev/video1`
- **Serial:** `/dev/ttyAMA10` (ArmPi controller)
- **Privileged Mode:** Full device access

## 🎯 Usage

### Starting ROS Nodes

Inside the container, use the provided startup script:

```bash
./start_node.sh
```

This script will:
- Source the ROS environment
- Set up proper environment variables
- Launch the main ArmPi FPV bringup sequence

### Available Launch Options

1. **Full System:** `roslaunch armpi_fpv_bringup bringup.launch`
2. **Camera Only:** `roslaunch armpi_fpv_bringup usb_cam.launch`
3. **MoveIt Demo:** `roslaunch armpi_fpv_moveit_config demo.launch`

### Development with Cursor IDE

1. Install the Remote SSH extension in Cursor IDE
2. Add SSH configuration:
   ```
   Host armpi-fpv
       HostName localhost  # or raspberrypidev
       Port 2222
       User ubuntu
   ```
3. Connect to the remote host
4. Open the workspace at `/home/ubuntu/armpi_fpv`

## 📁 Project Structure

```
/home/ubuntu/
├── armpi_fpv/          # Main ROS workspace
├── course/             # Tutorial and course materials
├── software/           # Additional software components
├── docker_src/         # Docker-related source files
└── start_node.sh       # ROS startup script
```

## 🔍 Troubleshooting

### Common Issues

**SSH Connection Failed:**
- Verify container is running: `docker ps`
- Check port mapping: ensure 2222 is not in use
- Try password authentication: `ubuntu`

**Camera Not Working:**
- Ensure camera devices are mapped: `--device=/dev/video0:/dev/video0`
- Check camera permissions in container
- Verify camera is connected to host

**ROS Nodes Failing:**
- Check if hardware devices are accessible
- Verify environment variables are set
- Review logs in `/root/.ros/log/`

### Container Management

**Stop Container:**
```bash
docker stop armpi-ssh-hardware
```

**Start Container:**
```bash
docker start armpi-ssh-hardware
```

**Remove Container:**
```bash
docker rm armpi-ssh-hardware
```

**View Logs:**
```bash
docker logs armpi-ssh-hardware
```

## 🧩 Installed Packages

### ROS Packages
- ros-noetic-desktop
- ros-noetic-moveit
- ros-noetic-industrial-core
- ros-noetic-rosbridge-server
- ros-noetic-usb-cam
- ros-noetic-web-video-server

### Python Packages
- roboticstoolbox-python
- modern-robotics
- opencv-python
- mediapipe
- ujson
- numpy, scipy, matplotlib
- And many more...

### System Tools
- SSH server with key authentication
- Oh-My-Zsh shell
- Git, Vim, Nano
- Development tools (build-essential, cmake)

## 🚧 Development

### Building Custom Images

Modify `Dockerfile.complete` and rebuild:

```bash
docker build -f Dockerfile.complete -t armpi-fpv-custom .
```

### Adding Dependencies

Add packages to the Dockerfile:

```dockerfile
RUN apt-get install -y your-package
# or
RUN pip3 install your-python-package
```

### Workspace Development

The ROS workspace is persistent in the container. Changes to code will be maintained between container restarts.

## 📞 Support

### Hardware Requirements
- ArmPi FPV robotic arm
- USB camera (compatible with Video4Linux)
- Raspberry Pi or compatible ARM64 system

### Software Versions
- ROS Noetic (Ubuntu 20.04 Focal)
- Python 3.8
- OpenCV 4.x

## 🏆 Features Achieved

✅ **SSH Remote Development** - Full IDE integration  
✅ **Hardware Access** - Camera and serial devices mapped  
✅ **ROS Environment** - Complete robotics development stack  
✅ **Web Interfaces** - Browser-based monitoring and control  
✅ **Package Management** - All dependencies pre-installed  
✅ **Easy Deployment** - One-command container startup  

---

**Ready to develop robotics applications with the ArmPi FPV!** 🤖✨
