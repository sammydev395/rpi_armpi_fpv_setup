# ArmPi FPV Docker - Quick Reference

## 🚀 Getting Started

```bash
# Build and run container
./run_armpi_container.sh

# Connect via SSH
ssh ubuntu@localhost -p 2222
```

## 🔗 Connection Details

| Service | Access | Credentials |
|---------|--------|-------------|
| SSH | `localhost:2222` | `ubuntu:ubuntu` |
| Web Video | `http://localhost:8080` | None |
| ROS Bridge | `ws://localhost:9090` | None |

## 🤖 ROS Commands

```bash
# Start full system
./start_node.sh

# Individual components
roslaunch armpi_fpv_bringup usb_cam.launch    # Camera only
roslaunch armpi_fpv_moveit_config demo.launch # MoveIt demo
```

## 🐳 Container Management

```bash
# Container control
docker start armpi-ssh-hardware
docker stop armpi-ssh-hardware
docker restart armpi-ssh-hardware

# Access container
docker exec -it armpi-ssh-hardware /bin/zsh

# View logs
docker logs armpi-ssh-hardware
```

## 💻 Cursor IDE Setup

1. Install Remote SSH extension
2. Add host configuration:
   ```
   Host armpi-fpv
       HostName localhost
       Port 2222
       User ubuntu
   ```
3. Connect to remote host
4. Open `/home/ubuntu/armpi_fpv`

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| SSH connection fails | Check container status: `docker ps` |
| Camera not working | Verify device mapping in run command |
| ROS nodes failing | Check hardware connections |
| Permission denied | Use `sudo` or check file permissions |

## 📁 Important Paths

- **Workspace:** `/home/ubuntu/armpi_fpv`
- **Logs:** `/root/.ros/log/`
- **Config:** `/home/ubuntu/armpi_fpv/src/armpi_fpv_bringup/`
