#!/bin/bash

# Script to install Docker on various Linux distributions
# This script is used by apsitv27-mysql when Docker is not found

# Function to check if a command exists
command_exists() {
    command -v "$1" > /dev/null 2>&1
}

# Function to detect OS
detect_os() {
    if [ -f /etc/os-release ]; then
        # freedesktop.org and systemd
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    elif type lsb_release >/dev/null 2>&1; then
        # linuxbase.org
        OS=$(lsb_release -si)
        VER=$(lsb_release -sr)
    elif [ -f /etc/lsb-release ]; then
        # For some versions of Debian/Ubuntu without lsb_release command
        . /etc/lsb-release
        OS=$DISTRIB_ID
        VER=$DISTRIB_RELEASE
    elif [ -f /etc/debian_version ]; then
        # Older Debian/Ubuntu/etc.
        OS=Debian
        VER=$(cat /etc/debian_version)
    else
        # Fall back to uname, e.g. "Linux <version>", also works for BSD
        OS=$(uname -s)
        VER=$(uname -r)
    fi
    
    echo "Detected OS: $OS $VER"
}

# Function to install Docker on Debian/Ubuntu
install_docker_debian() {
    echo "Installing Docker on Debian/Ubuntu..."
    
    # Update package index
    sudo apt-get update
    
    # Install packages to allow apt to use a repository over HTTPS
    sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    
    # Install Docker
    sudo apt-get install -y docker.io
    
    # Start and enable Docker service
    sudo systemctl enable docker
    sudo systemctl start docker
    
    # Add current user to the docker group
    username=$(whoami)
    sudo usermod -aG docker $username
    
    echo "Docker installed successfully!"
    echo "NOTE: You may need to log out and log back in for group changes to take effect."
}

# Function to install Docker on RHEL/CentOS/Fedora
install_docker_rhel() {
    echo "Installing Docker on RHEL/CentOS/Fedora..."
    
    # Install required packages
    if command_exists dnf; then
        sudo dnf -y install dnf-plugins-core
        sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
        sudo dnf install -y docker-ce docker-ce-cli containerd.io
    else
        sudo yum install -y yum-utils
        sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
        sudo yum install -y docker-ce docker-ce-cli containerd.io
    fi
    
    # Start and enable Docker service
    sudo systemctl enable docker
    sudo systemctl start docker
    
    # Add current user to the docker group
    username=$(whoami)
    sudo usermod -aG docker $username
    
    echo "Docker installed successfully!"
    echo "NOTE: You may need to log out and log back in for group changes to take effect."
}

# Main installation function
install_docker() {
    detect_os
    
    # Check if Docker is already installed
    if command_exists docker; then
        echo "Docker is already installed."
        return 0
    fi
    
    # Install Docker based on OS
    case "$OS" in
        *Ubuntu*|*Debian*|*Mint*)
            install_docker_debian
            ;;
        *Fedora*|*CentOS*|*Red\ Hat*|*RHEL*)
            install_docker_rhel
            ;;
        *)
            echo "Unsupported OS: $OS"
            echo "Please install Docker manually according to the official documentation:"
            echo "https://docs.docker.com/engine/install/"
            exit 1
            ;;
    esac
    
    # Verify installation
    if command_exists docker; then
        echo "Docker has been successfully installed!"
        docker --version
        
        # Attempt to run Docker
        echo "Verifying Docker can run..."
        if sudo docker run --rm hello-world 2>/dev/null; then
            echo "Docker is working correctly!"
        else
            echo "Docker installed but not running properly. You may need to start the service with 'sudo systemctl start docker'"
        fi
    else
        echo "Docker installation failed."
        exit 1
    fi
}

# Run the installation
install_docker
