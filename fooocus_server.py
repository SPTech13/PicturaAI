import os
import re
import subprocess
import time
from flask import Flask, jsonify

app = Flask(__name__)

# Define constants
FOOOCUS_REPO_URL = "https://github.com/lllyasviel/Fooocus.git"
FOOOCUS_DIR = "/tmp/Fooocus"
FOOOCUS_IP = None  # Will be set dynamically after Fooocus starts

def install_pygit2():
    """Install pygit2 if not already installed."""
    print("Installing pygit2...")
    result = subprocess.run(["pip", "install", "pygit2==1.15.1"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Error installing pygit2:", result.stderr)
        raise RuntimeError("Failed to install pygit2")

def clone_fooocus():
    """Clone the Fooocus repository if not already present."""
    if not os.path.exists(FOOOCUS_DIR):
        print("Cloning Fooocus repository...")
        result = subprocess.run(["git", "clone", FOOOCUS_REPO_URL, FOOOCUS_DIR], capture_output=True, text=True)
        if result.returncode != 0:
            print("Error cloning Fooocus repository:", result.stderr)
            raise RuntimeError("Failed to clone Fooocus repository")

def start_fooocus():
    """Start Fooocus and capture the IP address."""
    global FOOOCUS_IP

    print("Starting Fooocus...")
    command = ["python3", "entry_with_update.py", "--share", "--always-high-vram"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=FOOOCUS_DIR)

    # Monitor output for IP address
    while True:
        output = process.stdout.readline()
        if output == "" and process.poll() is not None:
            break
        if output:
            print(output.strip())  # Optional: Log output for debugging
            # Look for lines containing the IP address (e.g., "Running on https://1234-56-7890.ngrok.io")
            match = re.search(r"Running on (https?://[^\s]+)", output)
            if match:
                FOOOCUS_IP = match.group(1)
                print("Fooocus IP detected:", FOOOCUS_IP)
                break

    # If we haven't found the IP, Fooocus may not have started correctly
    if FOOOCUS_IP is None:
        raise RuntimeError("Failed to retrieve Fooocus IP address")

# Endpoint to get the Fooocus IP for the frontend
@app.route('/get_fooocus_ip', methods=['GET'])
def get_fooocus_ip():
    if FOOOCUS_IP:
        return jsonify({"success": True, "fooocus_ip": FOOOCUS_IP})
    return jsonify({"success": False, "message": "Fooocus IP not available"})

def initialize_fooocus():
    """Initialize Fooocus setup: install dependencies, clone repo, start Fooocus."""
    try:
        install_pygit2()
        clone_fooocus()
        start_fooocus()
    except RuntimeError as e:
        print("Initialization error:", str(e))
        return False
    return True

if __name__ == '__main__':
    # Initialize Fooocus before starting Flask server
    if initialize_fooocus():
        print("Fooocus setup complete. Starting Flask server.")
        app.run(host='0.0.0.0', port=5000)
    else:
        print("Fooocus setup failed.")
