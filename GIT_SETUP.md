# Git Repository Setup for ArmPi FPV Project

This document contains the information needed to set up the GitHub repositories for the ArmPi FPV Docker project.

## 📊 Repository Structure

### 1. Docker Setup Repository
- **Repository:** `git@github.com:sammydev395/rpi_armpi_fpv_setup.git`
- **Purpose:** Contains Docker configuration, build scripts, and documentation
- **Local Path:** `/home/sammydev295/armpi_docker_setup`

### 2. Container Contents Repository  
- **Repository:** `git@github.com:sammydev395/rpi_armpi_fpv.git`
- **Purpose:** Contains ROS workspace, source code, and applications
- **Local Path:** `/tmp/armpi_container_repo`

## 🔐 SSH Keys to Add to GitHub

### Key 1: For Docker Setup Repository (rpi_armpi_fpv_setup.git)
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPSkboQ8Rxr91yFniLoAI7T/RC6mPR+RTqZxFnrU/jsH sammydev295@raspberrypidev-armpi-setup
```

### Key 2: For Container Contents Repository (rpi_armpi_fpv.git)  
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHudwqwEmWacWeqGYu8gjFV9tEA9apRmUa+3sFKZp0h+ sammydev295@raspberrypidev-armpi-container
```

## 🚀 Setup Instructions

### Step 1: Add SSH Keys to GitHub
1. Go to GitHub.com → Settings → SSH and GPG keys
2. Click "New SSH key"
3. Add **Key 1** with title: "RaspberryPi ArmPi Setup"
4. Add **Key 2** with title: "RaspberryPi ArmPi Container"

### Step 2: Create GitHub Repositories
1. Create repository: `sammydev395/rpi_armpi_fpv_setup`
2. Create repository: `sammydev395/rpi_armpi_fpv`  
3. Both should be private repositories

### Step 3: Push Docker Setup Repository
```bash
cd /home/sammydev295/armpi_docker_setup
git remote add origin github-armpi-setup:sammydev395/rpi_armpi_fpv_setup.git
git branch -M main
git push -u origin main
```

### Step 4: Push Container Contents Repository
```bash
cd /tmp/armpi_container_repo
git remote add origin github-armpi-container:sammydev395/rpi_armpi_fpv.git
git branch -M main  
git push -u origin main
```

## 📁 Repository Contents

### Docker Setup Repository (`rpi_armpi_fpv_setup`)
- `Dockerfile.complete` - Complete Docker configuration
- `README.md` - Comprehensive documentation
- `QUICK_REFERENCE.md` - Quick command reference
- `run_armpi_container.sh` - Automated setup script
- `start_node.sh` - ROS startup script
- Build and configuration files

### Container Contents Repository (`rpi_armpi_fpv`)
- `armpi_fpv/` - ROS workspace with catkin packages
- `course/` - Tutorial materials and SDK
- `software/` - GUI control applications
- `docker_src/` - Container-specific scripts
- Built and tested ROS environment

## 🔧 SSH Configuration

The SSH config is already set up on the local machine:
- `github-armpi-setup` → Uses setup repository key
- `github-armpi-container` → Uses container repository key

## 🎯 Usage After Setup

Once repositories are created and pushed:

1. **Clone setup repository:**
   ```bash
   git clone git@github.com:sammydev395/rpi_armpi_fpv_setup.git
   cd rpi_armpi_fpv_setup
   ./run_armpi_container.sh
   ```

2. **Access container contents:**
   The container will automatically have the source code, or clone separately:
   ```bash
   git clone git@github.com:sammydev395/rpi_armpi_fpv.git
   ```

## ✅ Ready for Deployment

After completing these steps, you'll have:
- ✅ Version-controlled Docker environment
- ✅ Separate source code repository  
- ✅ SSH key authentication
- ✅ Complete documentation
- ✅ Automated deployment scripts

Both repositories are ready for collaboration and deployment! 🚀
