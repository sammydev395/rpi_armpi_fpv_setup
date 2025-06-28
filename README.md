# ArmPi FPV Docker Development Environment

Complete Docker setup for ArmPi FPV robot development with ROS Noetic, SSH access, and hardware integration.

## 🚀 Quick Start

### After Machine Reboot
```bash
cd ~/armpi_docker_setup
./run_armpi_container.sh
```

### SSH Access
```bash
# Local SSH access
ssh ubuntu@localhost -p 2222

# Remote SSH access (from Windows/other machines)
ssh ubuntu@<raspberry-pi-ip> -p 2222
```

## 📦 Current Setup Status

### ✅ Running Container
- **Name**: `armpi-ssh-hardware`
- **Image**: `armpi_ros_container:with-apriltag-mediapipe` (6.09GB)
- **Uptime**: Started 47+ hours ago
- **Status**: Running with full hardware access

### 🐳 Available Docker Images
| Image | Tag | Size | Description |
|-------|-----|------|-------------|
| `armpi_ros_container` | `with-apriltag-mediapipe` | 6.09GB | **Latest snapshot** with all packages |
| `armpi_fpv_ros` | `snapshot-20250625_185856` | 5.46GB | Previous snapshot |
| `armpi_fpv_ros` | `latest` | 5.22GB | Base build |

## 🔧 Container Features

### Installed Packages
- ✅ **ROS Noetic** (Desktop + MoveIt + Industrial)
- ✅ **AprilTag v3.x** (built from source - swatbotics/apriltag)
- ✅ **MediaPipe** (computer vision)
- ✅ **SSH Server** (remote development)
- ✅ **Git** (version control)
- ✅ **Python packages**: ujson, roboticstoolbox-python, etc.

### Hardware Access
- 📹 **Camera**: `/dev/video0`, `/dev/video1` (ArmPi FPV USB cameras)
- 🔌 **Serial**: `/dev/ttyAMA10` (robot control)
- 🖥️ **Display**: X11 forwarding enabled
- 💾 **Full access**: Privileged mode with `/dev` and `/sys` mounted

### Network Ports
| Port | Service | Description |
|------|---------|-------------|
| 2222 | SSH | Remote shell access |
| 8080 | Web Video | Camera stream web interface |
| 9090 | ROS Bridge | WebSocket ROS communication |
| 11311 | ROS Master | ROS core service |

## 🛠️ Management Scripts

### Primary Scripts
```bash
# Start container (after reboot or first time)
./run_armpi_container.sh

# Enter running container
./enter.sh

# Stop container
./stop.sh

# Start ROS services
./start_ros.sh
```

### Container Commands
```bash
# Shell access to running container
docker exec -it armpi-ssh-hardware /bin/zsh

# Start ROS nodes directly
docker exec armpi-ssh-hardware /home/ubuntu/start_node.sh

# Check container status
docker ps --filter name=armpi-ssh-hardware

# View container logs
docker logs armpi-ssh-hardware
```

## 🔐 SSH Configuration

### Authentication Methods
- **Username**: `ubuntu`
- **Password**: `ubuntu`
- **SSH Key**: Pre-configured for `sammy_o@win11`

### SSH Key Setup
```bash
# SSH keys are mounted from host
# Host keys: /home/sammydev295/.ssh
# Container keys: /home/ubuntu/.ssh_host (read-only)
```

## 🤖 ROS Environment

### Workspace Structure
```
/home/ubuntu/armpi_fpv/
├── src/          # ROS packages
├── build/        # Build artifacts  
├── devel/        # Development space
└── .git/         # Git repository
```

### Starting ROS
```bash
# Inside container
source /home/ubuntu/armpi_fpv/devel/setup.bash
roslaunch armpi_fpv_bringup armpi_fpv.launch

# Or use the script
/home/ubuntu/start_node.sh
```

## 🔄 Development Workflow

### 1. Connect with Cursor IDE
1. Install SSH extension in Cursor IDE
2. Connect to: `ubuntu@<raspberry-pi-ip>:2222`
3. Open workspace: `/home/ubuntu/armpi_fpv`

### 2. Git Operations
```bash
# Inside container
cd /home/ubuntu/armpi_fpv
git status
git add .
git commit -m "Your changes"
git push origin main
```

### 3. Testing Hardware
```bash
# Check cameras
ls -la /dev/video*

# Check serial device
ls -la /dev/ttyAMA10

# Test camera stream
roslaunch usb_cam usb_cam-test.launch
```

## 📋 Troubleshooting

### Container Won't Start
```bash
# Check if image exists
docker images | grep armpi

# Check for port conflicts
sudo netstat -tulpn | grep :2222

# Force restart
docker stop armpi-ssh-hardware
docker rm armpi-ssh-hardware
./run_armpi_container.sh
```

### SSH Connection Issues
```bash
# Test SSH locally first
ssh ubuntu@localhost -p 2222

# Check SSH service in container
docker exec armpi-ssh-hardware systemctl status ssh

# Verify SSH keys
docker exec armpi-ssh-hardware ls -la /home/ubuntu/.ssh/
```

### Hardware Access Problems
```bash
# Check device permissions
ls -la /dev/video* /dev/ttyAMA*

# Restart with privileged mode (already enabled)
./run_armpi_container.sh
```

### ROS Issues
```bash
# Source environment
source /home/ubuntu/armpi_fpv/devel/setup.bash

# Check ROS master
echo $ROS_MASTER_URI

# List ROS topics
rostopic list

# Check missing packages
rosdep check --from-paths src --ignore-src -r
```

## 📚 Additional Resources

### Documentation Files
- **HiWonder Guide**: Found in mounted system image at `/home/pi/Bookshelf/BeginnersGuide-5thEd-Eng_v3.pdf`
- **Setup Summary**: `SETUP_SUMMARY.md`
- **Git Guide**: `GIT_SETUP_GUIDE.md`

### Repository Links
- **Docker Setup**: `git@github.com:sammydev395/armpi_docker_setup.git`
- **Container Contents**: `git@github.com:sammydev395/armpi_container_repo.git`

### Key File Locations
```
~/armpi_docker_setup/        # This repository
├── Dockerfile               # Container build instructions
├── docker-compose.yml       # Alternative compose setup
├── run_armpi_container.sh   # Main startup script
├── start_node.sh            # ROS startup script
└── README.md               # This file
```

## 🎯 Next Steps

1. **After Reboot**: Run `./run_armpi_container.sh`
2. **Connect IDE**: SSH to `ubuntu@<pi-ip>:2222`
3. **Start Development**: Open `/home/ubuntu/armpi_fpv` in Cursor IDE
4. **Test Hardware**: Run camera and servo tests
5. **Start Coding**: Begin your ArmPi FPV projects!

---

**Last Updated**: June 28, 2025  
**Container Version**: `armpi_ros_container:with-apriltag-mediapipe`  
**Environment**: Raspberry Pi 4 + Ubuntu + Docker + ROS Noetic
