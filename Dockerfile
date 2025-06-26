FROM ros:noetic
# Install ROS desktop packages first
RUN apt-get update && apt-get install -y ros-noetic-desktop ros-noetic-moveit ros-noetic-industrial-core && rm -rf /var/lib/apt/lists/*


# Install system dependencies including SSH server
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    python3-rosdep \
    python3-rosinstall \
    python3-rosinstall-generator \
    python3-wstool \
    build-essential \
    cmake \
    git \
    curl \
    wget \
    vim \
    nano \
    zsh \
    sudo \
    udev \
    v4l-utils \
    libv4l-dev \
    pkg-config \
    libgtk-3-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libtbb2 \
    libtbb-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libdc1394-22-dev \
    libusb-1.0-0-dev \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

# Configure SSH
RUN mkdir /var/run/sshd
RUN echo 'root:rootpassword' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

# Install Python packages commonly used in ROS robotics
RUN pip3 install \
    numpy \
    opencv-python \
    scipy \
    matplotlib \
    Pillow \
    pyserial \
    pygame \
    pynput \
    roboticstoolbox-python \
    modern-robotics \
    transforms3d \
    pyyaml \
    rospkg \
    catkin-tools

# Create non-root user with password for SSH access
RUN useradd -m -s /bin/zsh ubuntu && \
    echo "ubuntu ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    usermod -aG dialout ubuntu && \
    echo 'ubuntu:ubuntu' | chpasswd

# Install oh-my-zsh for ubuntu user
USER ubuntu
WORKDIR /home/ubuntu
RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Setup Git configuration and SSH for ubuntu user
RUN git config --global user.name "ArmPi Developer" && \
    git config --global user.email "sammydev395@users.noreply.github.com" && \
    git config --global init.defaultBranch main

# Create SSH directory and copy SSH keys
RUN mkdir -p ~/.ssh && chmod 700 ~/.ssh

# Copy the ArmPi FPV workspace
COPY --chown=ubuntu:ubuntu armpi_fpv /home/ubuntu/armpi_fpv
COPY --chown=ubuntu:ubuntu course /home/ubuntu/course
COPY --chown=ubuntu:ubuntu software /home/ubuntu/software
COPY --chown=ubuntu:ubuntu docker_src /home/ubuntu/docker_src

# Initialize rosdep (as root)
USER root
RUN rosdep init || true && rosdep update

# Switch back to ubuntu user
USER ubuntu

# Update rosdep for user
RUN rosdep update

# Build the workspace
WORKDIR /home/ubuntu/armpi_fpv
# Clean workspace and fix permissions
RUN rm -rf build devel logs .catkin_tools || true
RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && catkin_make clean && catkin_make"

# Setup ROS environment in zshrc
RUN echo "source /opt/ros/noetic/setup.zsh" >> ~/.zshrc && \
    echo "source ~/armpi_fpv/devel/setup.zsh" >> ~/.zshrc && \
    echo "export ROS_MASTER_URI=http://localhost:11311" >> ~/.zshrc && \
    echo "export ROS_HOSTNAME=localhost" >> ~/.zshrc

# Initialize Git repository in the workspace and fix ownership
WORKDIR /home/ubuntu/armpi_fpv
RUN git init && \
    git remote remove origin || true && \
    git remote add origin git@github.com:sammydev395/rpi_armpi_fpv.git && \
    git config --global --add safe.directory /home/ubuntu/armpi_fpv

# Copy startup script if it exists
COPY --chown=ubuntu:ubuntu start_node.sh /home/ubuntu/start_node.sh

# Create a startup script to run SSH daemon and keep container running
USER root
RUN echo '#!/bin/bash\n/usr/sbin/sshd -D &\nsu - ubuntu -c "cd /home/ubuntu && exec $@"' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Expose SSH port
EXPOSE 22

WORKDIR /home/ubuntu
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/bin/zsh"]
