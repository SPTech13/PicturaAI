import os
import re
import subprocess
import time
from flask import Flask, jsonify

app = Flask(__name__)

# Define constants
FOOOCUS_REPO_URL = "https://github.com/lllyasviel/Fooocus.git"
FOOOCUS_DIR = "/tmp/Fooocus"
FOOOCUS_IP = "http://localhost:5001"  # Fallback IP for testing if Fooocus fails to provide one

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
    log_file = "/tmp/fooocus_startup.log"  # Log file to capture all output

    print("Starting Fooocus...")
    command = ["python3", "entry_with_update.py", "--share", "--always-high-vram"]
    with open(log_file, "w") as logfile:
        process = subprocess.Popen(command, stdout=logfile, stderr=logfile, text=True, cwd=FOOOCUS_DIR)

    # Wait for Fooocus to initialize
    process.wait(timeout=60)

    # Read the log file to search for the IP address
    with open(log_file, "r") as logfile:
        all_output = logfile.readlines()

    # Print output to Render logs and attempt to find the IP
    print("Full Fooocus startup log:")
    for line in all_output:
        print(line.strip())  # Print each line of the log for review

        # Attempt to find IP address in output
        match = re.search(r"Running on (https?://[^\s]+)", line)
        if match:
            FOOOCUS_IP = match.group(1)
            print("Fooocus IP detected:", FOOOCUS_IP)
            break

    if FOOOCUS_IP == "http://localhost:5001":
        print("Using fallback Fooocus IP:", FOOOCUS_IP)
    if FOOOCUS_IP is None:
        raise RuntimeError("Failed to retrieve Fooocus IP address after reviewing the full log.")

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
        # Bind Flask to port 8080 for Render
        app.run(host='0.0.0.0', port=8080)
    else:
        print("Fooocus setup failed.")
