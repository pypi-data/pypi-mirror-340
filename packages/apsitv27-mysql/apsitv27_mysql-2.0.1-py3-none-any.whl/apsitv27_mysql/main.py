import os
import subprocess
import time
import platform
import shutil
import sys
import getpass

# Constants for better maintainability
CONTAINER_NAME = "my-persistent-mysql"
IMAGE_NAME = "apsitv27-mysql"
VOLUME_NAME = "mysql_data"
MYSQL_ROOT_PASSWORD = "1234"

def check_and_install_docker():
    """Check if Docker is installed and install if needed."""
    try:
        # Check if Docker is installed
        subprocess.check_call(["docker", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ System environment verified.")
        return True
    except FileNotFoundError:
        # Docker is not installed
        print("⚠️ Required system components not found (Docker).")
        
        if platform.system() == "Linux":
            print("\nAttempting to install Docker automatically...")
            try:
                # Try to detect the Linux distribution
                if os.path.exists("/etc/debian_version") or os.path.exists("/etc/ubuntu_version"):
                    # Debian/Ubuntu-based
                    print("Detected Debian/Ubuntu-based distribution.")
                    print("Installing Docker using apt...")
                    
                    # Update package lists
                    subprocess.check_call(["sudo", "apt", "update"])
                    
                    # Install Docker
                    subprocess.check_call(["sudo", "apt", "install", "-y", "docker.io"])
                    
                    # Start and enable Docker service
                    subprocess.check_call(["sudo", "systemctl", "enable", "docker"])
                    subprocess.check_call(["sudo", "systemctl", "start", "docker"])
                    
                    # Add current user to the docker group to avoid permission issues
                    username = getpass.getuser()
                    try:
                        subprocess.check_call(["sudo", "usermod", "-aG", "docker", username])
                        print(f"\n✅ Added user '{username}' to the docker group.")
                        print("⚠️ You MUST start a new terminal session for the group changes to take effect.")
                        print("After starting a new terminal, run 'apsitv27-mysql' again.\n")
                        return False
                    except subprocess.CalledProcessError:
                        print("Failed to add user to docker group. You might need to run Docker with sudo.")
                
                elif os.path.exists("/etc/redhat-release"):
                    # RHEL/CentOS/Fedora
                    print("Detected RHEL/CentOS/Fedora-based distribution.")
                    print("Installing Docker using dnf/yum...")
                    
                    # Install Docker
                    if shutil.which("dnf"):
                        subprocess.check_call(["sudo", "dnf", "install", "-y", "docker"])
                    else:
                        subprocess.check_call(["sudo", "yum", "install", "-y", "docker"])
                    
                    # Start and enable Docker service
                    subprocess.check_call(["sudo", "systemctl", "enable", "docker"])
                    subprocess.check_call(["sudo", "systemctl", "start", "docker"])
                    
                    # Add current user to the docker group
                    username = getpass.getuser()
                    try:
                        subprocess.check_call(["sudo", "usermod", "-aG", "docker", username])
                        print(f"\n✅ Added user '{username}' to the docker group.")
                        print("⚠️ You MUST log out and log back in for the group changes to take effect.")
                        print("After logging back in, run 'apsitv27-mysql' again.\n")
                        return False
                    except subprocess.CalledProcessError:
                        print("Failed to add user to docker group. You might need to run Docker with sudo.")
                
                else:
                    print("Unsupported Linux distribution for automatic installation.")
                    print("\nPlease install Docker manually:")
                    print("1. For Ubuntu/Debian: sudo apt install docker.io")
                    print("2. For RHEL/CentOS/Fedora: sudo dnf install docker")
                    print("3. For other distributions, visit: https://docs.docker.com/engine/install/")
                    return False
                
            except subprocess.CalledProcessError as e:
                print(f"Error during Docker installation: {e}")
                print("\nPlease install Docker manually:")
                print("1. For Ubuntu/Debian: sudo apt install docker.io")
                print("2. For RHEL/CentOS/Fedora: sudo dnf install docker")
                print("3. For other distributions, visit: https://docs.docker.com/engine/install/")
                return False
                
        elif platform.system() == "Windows":
            print("\nPlease install Docker Desktop for Windows manually:")
            print("1. Download from: https://www.docker.com/products/docker-desktop")
            print("2. Run the installer and follow the installation instructions")
            print("3. Start Docker Desktop from the Start menu")
            print("4. After installation, run 'apsitv27-mysql' again")
            return False
            
        elif platform.system() == "Darwin":  # macOS
            print("\nPlease install Docker Desktop for Mac manually:")
            print("1. Download from: https://www.docker.com/products/docker-desktop")
            print("2. Install the application")
            print("3. Start Docker Desktop from the Applications folder")
            print("4. After installation, run 'apsitv27-mysql' again")
            return False
            
        return False

def check_and_start_docker():
    """Check if Docker service is running and start it if not."""
    try:
        # Check if Docker is running
        subprocess.check_call(["docker", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ Service engine is active.")
        return True
    except subprocess.CalledProcessError:
        # Docker is installed but not running or permission issues
        # First, let's check if it's a permission issue
        try:
            result = subprocess.run(["docker", "info"], stderr=subprocess.PIPE, text=True)
            error_msg = result.stderr.lower()
            
            if "permission denied" in error_msg and "docker.sock" in error_msg:
                print("\n⚠️ Permission denied when accessing Docker socket.")
                print("You need to add your user to the 'docker' group.")
                
                username = getpass.getuser()
                try:
                    print(f"Attempting to add user '{username}' to the docker group...")
                    subprocess.check_call(["sudo", "usermod", "-aG", "docker", username])
                    print(f"\n✅ Successfully added user '{username}' to the docker group.")
                    print("⚠️ You MUST log out and log back in for the group changes to take effect.")
                    print("After logging back in, run 'apsitv27-mysql' again.\n")
                except subprocess.CalledProcessError:
                    print(f"\nFailed to add user to docker group automatically.")
                    print("Please run this command manually:")
                    print(f"    sudo usermod -aG docker {username}")
                    print("Then log out and log back in for the changes to take effect.")
                    print("After logging back in, run 'apsitv27-mysql' again.\n")
                return False
            
        except Exception:
            # Fallback to the general case if we can't determine the specific error
            pass
            
        # Docker is installed but not running (not a permission issue)
        if platform.system() == "Linux":
            print("\nDocker is installed but not running. Attempting to start Docker service...")
            try:
                subprocess.check_call(["sudo", "systemctl", "start", "docker"])
                print("Docker service started successfully.")
                
                # Give the service a moment to fully start
                print("Waiting for Docker service to become fully available...")
                for i in range(5):
                    time.sleep(1)
                    try:
                        subprocess.check_call(["docker", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        print("Service engine is now running.")
                        return True
                    except subprocess.CalledProcessError:
                        pass
                    
                print("Service started but not yet responding. You may need to wait a moment.")
                return False
                
            except subprocess.CalledProcessError:
                print("Failed to start Docker. Please start the Docker service manually using:")
                print("sudo systemctl start docker\n")
                return False
        elif platform.system() == "Windows":
            print("\nDocker Desktop is not running. Please start Docker Desktop manually.")
            print("Open Docker Desktop from the Start menu and ensure the engine is running.")
            return False
        elif platform.system() == "Darwin":  # macOS
            print("\nDocker Desktop is not running. Please start Docker Desktop manually.")
            print("Open Docker Desktop from the Applications folder and ensure the engine is running.")
            return False
    
    return False

def ensure_docker_files_exist():
    """Ensure Docker files exist and are properly formatted."""
    package_dir = os.path.dirname(__file__)
    entrypoint_path = os.path.join(package_dir, "entrypoint.sh")
    dockerfile_path = os.path.join(package_dir, "dockerfile")
    dockerfile_caps_path = os.path.join(package_dir, "Dockerfile")
    
    # Check for Dockerfile existence
    if not os.path.exists(dockerfile_path) and not os.path.exists(dockerfile_caps_path):
        print("⚠️ Dockerfile not found in package directory.")
        return False
        
    # Check for entrypoint.sh existence
    if not os.path.exists(entrypoint_path):
        print("⚠️ entrypoint.sh not found in package directory.")
        return False
        
    # Make sure entrypoint.sh is executable on Unix-like systems
    if platform.system() != "Windows" and os.path.exists(entrypoint_path):
        try:
            current_mode = os.stat(entrypoint_path).st_mode
            os.chmod(entrypoint_path, current_mode | 0o111)  # Add execute permission
        except Exception:
            print("Note: Could not set executable permission on entrypoint.sh")
    
    # Fix line endings for entrypoint.sh if on Windows
    if platform.system() == "Windows" and os.path.exists(entrypoint_path):
        try:
            with open(entrypoint_path, 'r') as f:
                content = f.read()
            
            # Fix line endings (convert CRLF to LF)
            if '\r\n' in content:
                content = content.replace('\r\n', '\n')
                with open(entrypoint_path, 'w', newline='\n') as f:
                    f.write(content)
                print("✓ Configuration scripts optimized for compatibility.")
        except Exception as e:
            print(f"Note: Could not optimize script file format: {e}")
    
    return True

def build_and_run_mysql_container():
    """Main function to build and run MySQL container."""
    # Check if Docker is installed, and install if needed
    if not check_and_install_docker():
        print("\n⚠️ System configuration incomplete. Please address the issues above and try again.")
        return 1

    # Ensure Docker is running
    if not check_and_start_docker():
        print("\n⚠️ Service engine not running. Please address the issues above and try again.")
        return 1

    # Verify required files exist
    if not ensure_docker_files_exist():
        print("\n⚠️ Required package files are missing. Please reinstall the package.")
        return 1

    try:
        # Step 1: Check if the image exists
        try:
            existing_image = subprocess.check_output([
                "docker", "images", "-q", IMAGE_NAME
            ]).strip().decode()
        except subprocess.CalledProcessError:
            existing_image = None

        # Step 2: Build the Docker image if it doesn't exist
        if not existing_image:
            print("➤ Setting up MySQL environment...")
            print("   Please wait, this may take a moment...")
            
            package_dir = os.path.dirname(__file__)
            
            try:
                # Build the Docker image
                result = subprocess.run(
                    ["docker", "build", "-t", IMAGE_NAME, package_dir],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                if result.returncode != 0:
                    # If build fails, provide helpful error message
                    print(f"\n⚠️ Failed to set up MySQL environment: {result.stderr}")
                    
                    # Handle common errors
                    if "permission denied" in result.stderr.lower():
                        if platform.system() == "Windows":
                            print("\nTry running in an elevated (Administrator) PowerShell or Command Prompt.")
                        else:
                            print("Try running with 'sudo' if you have permission issues:")
                            print(f"sudo -E {' '.join(sys.argv)}")
                    elif "no such file" in result.stderr.lower():
                        print("\nMissing required files. Please reinstall the package.")
                    else:
                        print("\nPlease ensure Docker is properly configured and try again.")
                        
                    return 1
            except Exception as e:
                print(f"\n⚠️ Error during setup: {e}")
                return 1
        else:
            print("✓ MySQL environment is ready.")

        # Step 3: Check if the container exists
        try:
            existing_container = subprocess.check_output([
                "docker", "ps", "-aq", "--filter", f"name={CONTAINER_NAME}"
            ]).strip().decode()
        except subprocess.CalledProcessError:
            existing_container = None

        # Step 4: Stop and remove existing container if it exists
        if existing_container:
            print("➤ Stopping previous MySQL instance...")
            try:
                subprocess.check_call(["docker", "rm", "-f", CONTAINER_NAME])
            except subprocess.CalledProcessError as e:
                print(f"\n⚠️ Failed to stop previous MySQL instance: {e}")
                return 1

        # Step 5: Run a new container
        print("➤ Starting MySQL server with persistent storage...")
        try:
            subprocess.check_call([
                "docker", "run", "-it", "--name", CONTAINER_NAME, 
                "-v", f"{VOLUME_NAME}:/var/lib/mysql", 
                "-e", f"MYSQL_ROOT_PASSWORD={MYSQL_ROOT_PASSWORD}", 
                IMAGE_NAME
            ])
        except subprocess.CalledProcessError as e:
            print(f"\n⚠️ Failed to start MySQL server: {e}")
            
            # If the first attempt fails due to entrypoint issues, try a simpler approach
            if "entrypoint" in str(e).lower():
                print("\nTrying with alternate configuration...")
                try:
                    subprocess.check_call([
                        "docker", "run", "-it", "--name", CONTAINER_NAME, 
                        "-v", f"{VOLUME_NAME}:/var/lib/mysql", 
                        "-e", f"MYSQL_ROOT_PASSWORD={MYSQL_ROOT_PASSWORD}",
                        "-e", "MYSQL_DATABASE=mydb", 
                        "mysql:8.0"
                    ])
                    return 0
                except subprocess.CalledProcessError:
                    print("\n⚠️ Failed to start MySQL with alternate configuration.")
            
            # Provide helpful error messages
            if platform.system() == "Windows":
                print("Try running in an elevated (Administrator) PowerShell or Command Prompt.")
            else:
                print("Try running with 'sudo' if you have permission issues:")
                print(f"sudo -E {' '.join(sys.argv)}")
            return 1

    except KeyboardInterrupt:
        # Gracefully handle CTRL+C
        print("\nProcess interrupted. Cleaning up...")
        try:
            print("Shutting down MySQL server...")
            subprocess.check_call(["docker", "rm", "-f", CONTAINER_NAME], 
                                 stdout=subprocess.DEVNULL, 
                                 stderr=subprocess.DEVNULL)
            print("MySQL server stopped.")
        except:
            pass
        return 0

    return 0

if __name__ == "__main__":
    sys.exit(build_and_run_mysql_container())
