import os
import subprocess
import time
import platform
import shutil
import sys
import getpass

def check_and_install_docker():
    try:
        # Check if Docker is installed
        subprocess.check_call(["docker", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ System environment verified.")
        return True
    except FileNotFoundError:
        # Docker is not installed
        print("⚠️ Required system components not found.")
        
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
                        print("⚠️ You MUST Start a new terminal session for the group changes to take effect.")
                        print("After logging back in, run 'apsitv27-mysql' again.\n")
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
                        print("⚠️ You MUST log out and log back in (or restart the system) for the group changes to take effect.")
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
                    print("⚠️ You MUST log out and log back in (or restart the system) for the group changes to take effect.")
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
                        print("Docker engine is now running.")
                        return True
                    except subprocess.CalledProcessError:
                        pass
                    
                print("Docker service started but not yet responding. You may need to wait a moment.")
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

def build_and_run_mysql_container():
    container_name = "my-persistent-mysql"
    image_name = "apsitv27-mysql"
    volume_name = "mysql_data"
    mysql_root_password = "1234"

    # Check if Docker is installed, and install if needed
    if not check_and_install_docker():
        print("\n⚠️ System configuration incomplete. Please address the issues above and try again.")
        return 1

    # Ensure Docker is running
    if not check_and_start_docker():
        print("\n⚠️ Service engine not running. Please address the issues above and try again.")
        return 1

    try:
        # Step 1: Verify required files exist
        package_dir = os.path.dirname(__file__)
        entrypoint_path = os.path.join(package_dir, "entrypoint.sh")
        dockerfile_path = os.path.join(package_dir, "dockerfile")
        
        if platform.system() == "Windows":
            # For Windows, check case-insensitively for Dockerfile/dockerfile
            dockerfile_exists = os.path.exists(dockerfile_path) or os.path.exists(os.path.join(package_dir, "Dockerfile"))
            if not dockerfile_exists:
                print(f"\n⚠️ Error: Dockerfile not found in {package_dir}")
                print("Please ensure both 'Dockerfile' and 'entrypoint.sh' files are properly installed with the package.")
                return 1
        else:
            if not os.path.exists(dockerfile_path):
                print(f"\n⚠️ Error: dockerfile not found in {package_dir}")
                print("Please ensure both 'dockerfile' and 'entrypoint.sh' files are properly installed with the package.")
                return 1
                
        if not os.path.exists(entrypoint_path):
            print(f"\n⚠️ Error: entrypoint.sh not found in {package_dir}")
            print("Please ensure both 'dockerfile' and 'entrypoint.sh' files are properly installed with the package.")
            return 1
            
        # Make sure entrypoint.sh is executable
        if platform.system() != "Windows":
            try:
                subprocess.check_call(["chmod", "+x", entrypoint_path])
            except subprocess.CalledProcessError:
                print("Note: Could not set executable permission on entrypoint.sh")

        # Step 2: Check if the image exists
        try:
            existing_image = subprocess.check_output([
                "docker", "images", "-q", image_name
            ]).strip().decode()
        except subprocess.CalledProcessError:
            existing_image = None

        # Build the Docker image only if it doesn't exist
        if not existing_image:
            print("➤ Initializing MySQL server environment...")
            
            # Fix line endings for entrypoint.sh if on Windows
            if platform.system() == "Windows":
                try:
                    # Read the file content
                    with open(entrypoint_path, 'r') as f:
                        content = f.read()
                    
                    # Fix line endings (convert CRLF to LF)
                    content = content.replace('\r\n', '\n')
                    
                    # Write back
                    with open(entrypoint_path, 'w', newline='\n') as f:
                        f.write(content)
                    
                    print("✓ Configuration scripts optimized for compatibility.")
                except Exception as e:
                    print(f"Note: Configuration optimization skipped: {e}")
            
            # Print the dockerfile location for debugging (remove or make less technical)
            # print(f"Using configuration from: {package_dir}")
            
            try:
                # Use subprocess.run with capture_output to get detailed error info if needed
                print("   Please wait, this may take a moment...")
                process = subprocess.run(
                    ["docker", "build", "-t", image_name, package_dir],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                if process.returncode != 0:
                    print(f"\n⚠️ Failed to initialize MySQL server: {process.stderr}")
                    if "no such file or directory" in process.stderr.lower():
                        print("\nFile not found error during build.")
                        print("Creating a debug log file with build context information...")
                        try:
                            with open(os.path.join(os.getcwd(), "docker_build_debug.log"), "w") as f:
                                f.write("Docker build directory contents:\n")
                                f.write("-" * 50 + "\n")
                                for root, dirs, files in os.walk(package_dir):
                                    f.write(f"Directory: {root}\n")
                                    for file in files:
                                        f.write(f"  - {file}\n")
                                f.write("\nDocker build error:\n")
                                f.write("-" * 50 + "\n")
                                f.write(process.stderr)
                            print(f"Debug log written to {os.path.join(os.getcwd(), 'docker_build_debug.log')}")
                        except Exception as e:
                            print(f"Failed to write debug log: {e}")
                    
                    if platform.system() == "Windows":
                        print("\nWindows-specific fix attempt:")
                        print("Trying a different approach to build the Docker image...")
                        
                        # Create a temporary build context directory
                        temp_dir = os.path.join(os.path.dirname(package_dir), "temp_docker_build")
                        os.makedirs(temp_dir, exist_ok=True)
                        
                        # Copy the necessary files to the temp directory
                        with open(os.path.join(temp_dir, "Dockerfile"), 'w', newline='\n') as f:
                            f.write("FROM mysql:8.0\n\n")
                            f.write("ENV MYSQL_ROOT_PASSWORD=1234\n")
                            f.write("ENV MYSQL_DATABASE=mydb\n\n")
                            f.write("VOLUME [\"/var/lib/mysql\"]\n\n")
                            f.write("COPY entrypoint.sh /entrypoint.sh\n")
                            f.write("RUN chmod +x /entrypoint.sh\n\n")
                            f.write("EXPOSE 3306\n\n")
                            f.write("ENTRYPOINT [\"/entrypoint.sh\"]\n\n")
                            f.write("CMD [\"mysqld\"]\n")
                        
                        # Copy entrypoint.sh with LF line endings
                        with open(entrypoint_path, 'r') as src:
                            content = src.read()
                        with open(os.path.join(temp_dir, "entrypoint.sh"), 'w', newline='\n') as dest:
                            dest.write(content)
                        
                        print(f"Temporary build context created at {temp_dir}")
                        print("Attempting build with the temporary context...")
                        
                        alt_build = subprocess.run(
                            ["docker", "build", "-t", image_name, temp_dir],
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE,
                            text=True
                        )
                        
                        if alt_build.returncode == 0:
                            print("Alternative build approach successful!")
                        else:
                            print(f"\n⚠️ Alternative build also failed: {alt_build.stderr}")
                            print("Try running in an elevated (Administrator) PowerShell or Command Prompt.")
                            
                            # Add even more debugging info
                            print("\nDebug information:")
                            print(f"Package directory: {package_dir}")
                            print(f"Files in package directory: {os.listdir(package_dir)}")
                            print(f"Entrypoint.sh exists: {os.path.exists(entrypoint_path)}")
                            if os.path.exists(entrypoint_path):
                                print(f"Entrypoint.sh size: {os.path.getsize(entrypoint_path)} bytes")
                            return 1
                    else:
                        print("Try running with 'sudo' if you have permission issues:")
                        print(f"sudo -E {' '.join(sys.argv)}")
                    return 1
                    
            except Exception as e:
                print(f"\n⚠️ Exception during initialization: {e}")
                return 1
        else:
            print("✓ MySQL server environment already configured.")

        # Step 3: Check if the container exists
        try:
            existing_container = subprocess.check_output([
                "docker", "ps", "-aq", "--filter", f"name={container_name}"
            ]).strip().decode()
        except subprocess.CalledProcessError:
            existing_container = None

        # Step 4: Stop and remove existing container (if needed)
        if existing_container:
            print("➤ Stopping previous MySQL instance...")
            try:
                subprocess.check_call(["docker", "rm", "-f", container_name])
            except subprocess.CalledProcessError as e:
                print(f"\n⚠️ Failed to stop previous MySQL instance: {e}")
                if platform.system() == "Windows":
                    print("Try running in an elevated (Administrator) PowerShell or Command Prompt.")
                else:
                    print("Try running with 'sudo' if you have permission issues:")
                    print(f"sudo -E {' '.join(sys.argv)}")
                return 1

        # Step 5: Run a new container interactively (attached mode)
        print("➤ Starting MySQL server with persistent storage...")
        try:
            process = subprocess.run([
                "docker", "run", "-it", "--name", container_name, "-v",
                f"{volume_name}:/var/lib/mysql", "-e", f"MYSQL_ROOT_PASSWORD={mysql_root_password}", image_name
            ], stderr=subprocess.PIPE, text=True)
            
            if process.returncode != 0:
                print(f"\n⚠️ Failed to start MySQL server: {process.stderr}")
                if "no such file or directory" in process.stderr.lower() and "entrypoint" in process.stderr.lower():
                    print("\nEntrypoint script issue detected. This might be due to:")
                    print("1. Line ending issues (CR/LF vs LF)")
                    print("2. File permissions")
                    print("3. File encoding")
                    
                    print("\nTrying to fix the issue automatically...")
                    
                    # Remove the image to force a rebuild
                    subprocess.run(["docker", "rmi", "-f", image_name], 
                                 stdout=subprocess.DEVNULL, 
                                 stderr=subprocess.DEVNULL)
                    
                    print("Please run the command again. If the issue persists, try:")
                    print("1. Check your MySQL configuration file format")
                    print("2. Re-install the package")
                    
                if platform.system() == "Windows":
                    print("\nWindows-specific issue: Docker may have trouble with paths or file permissions.")
                    print("Try running in an elevated (Administrator) PowerShell or Command Prompt.")
                else:
                    print("Try running with 'sudo' if you have permission issues:")
                    print(f"sudo -E {' '.join(sys.argv)}")
                return 1
                
        except subprocess.CalledProcessError as e:
            print(f"\n⚠️ Failed to start MySQL server: {e}")
            if platform.system() == "Windows":
                print("Windows-specific issue: Docker may have trouble with paths or file permissions.")
                print("Try running in an elevated (Administrator) PowerShell or Command Prompt.")
            else:
                print("Try running with 'sudo' if you have permission issues:")
                print(f"sudo -E {' '.join(sys.argv)}")
            return 1

    except KeyboardInterrupt:
        # Gracefully handle CTRL+C
        print("\nProcess interrupted by the user. Cleaning up...")
        try:
            print("Shutting down MySQL server...")
            subprocess.check_call(["docker", "rm", "-f", container_name])
            print("MySQL server stopped successfully.")
        except subprocess.CalledProcessError:
            print("Error stopping the MySQL server.")
        finally:
            return 0

    return 0

if __name__ == "__main__":
    sys.exit(build_and_run_mysql_container())
