import os
import subprocess
import sys

# Function to run a system command and handle errors
def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        sys.exit(1)

# Step 1: Check for Python 3.11.x and CUDA 11.8 installation
print("Ensure Python 3.11.x and CUDA 11.8 are installed.")
python_version = sys.version.split()[0]

# Validate that the installed Python version is 3.11.x
if not python_version.startswith("3.11"):
    print("Please install Python 3.11.x to continue.")
    sys.exit(1)

# Step 2: Install PyTorch with CUDA 11.8 support
print("\nInstalling PyTorch with CUDA 11.8 support...")
run_command("py -3.11 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")

# Step 3: Install project dependencies from requirements.txt
print("\nInstalling project dependencies...")
if not os.path.exists("requirements.txt"):
    print("requirements.txt not found. Please make sure it exists in the directory.")
    sys.exit(1)

# Execute the command to install the required dependencies
run_command("py -3.11 -m pip install -r requirements.txt")

# Step 4: Confirm that the setup is complete
print("\nSetup complete. Ensure Counter-Strike 1.6 is running in windowed mode before starting the aimbot.")

# Step 5: Start the main Python script
print("\nStarting the aimbot script...")
run_command("py -3.11 main.py")
