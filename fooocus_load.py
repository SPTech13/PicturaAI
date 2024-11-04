import subprocess
import os
import sys

def run_command(command, cwd=None):
    """Helper function to run a shell command and print the output in real time."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=cwd)
    
    # Stream output to the console
    while True:
        output = process.stdout.readline().decode("utf-8")
        if output == "" and process.poll() is not None:
            break
        if output:
            print(output.strip())
    
    # Capture any errors
    stderr = process.stderr.read().decode("utf-8")
    if stderr:
        print("Error:", stderr)
    
    return process.returncode

# Step 1: Install pygit2
print("Installing pygit2...")
result = run_command("pip install pygit2==1.15.1")
if result != 0:
    sys.exit("Failed to install pygit2. Exiting.")

# Step 2: Clone the Fooocus repository
print("Cloning the Fooocus repository...")
fooocus_dir = "/tmp/Fooocus"  # You can change this path if desired
if not os.path.exists(fooocus_dir):
    result = run_command(f"git clone https://github.com/lllyasviel/Fooocus.git {fooocus_dir}")
    if result != 0:
        sys.exit("Failed to clone the Fooocus repository. Exiting.")
else:
    print("Fooocus repository already exists.")

# Step 3: Run the Fooocus Python script
print("Running entry_with_update.py...")
result = run_command("python3 entry_with_update.py --share --always-high-vram", cwd=fooocus_dir)
if result != 0:
    sys.exit("Failed to run entry_with_update.py. Exiting.")

print("Fooocus setup completed successfully.")
