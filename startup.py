import subprocess
import time

def initialize_fooocus():
    """Run Fooocus initialization in the background."""
    print("Initializing Fooocus...")
    # Run fooocus_server.py which includes Fooocus setup
    process = subprocess.Popen(["python3", "./fooocus_server.py"])
    time.sleep(5)  # Wait a few seconds to ensure Fooocus starts
    return process

def start_gunicorn():
    """Start Gunicorn to serve the Flask app."""
    print("Starting Flask app with Gunicorn...")
    # Run Gunicorn to serve the app
    subprocess.run(["gunicorn", "--bind", "0.0.0.0:8080", "fooocus_server:app"])

if __name__ == "__main__":
    fooocus_process = initialize_fooocus()  # Initialize Fooocus
    start_gunicorn()  # Start the Flask app with Gunicorn

    # Optionally, wait for Fooocus initialization to complete if needed
    fooocus_process.wait()
