#!/bin/bash

# Install pygit2
echo "Installing pygit2..."
pip install pygit2==1.15.1
if [ $? -ne 0 ]; then
    echo "Failed to install pygit2" >&2
    exit 1
fi

# Clone the Fooocus repository if it doesn't already exist
if [ ! -d "/tmp/Fooocus" ]; then
    echo "Cloning Fooocus repository..."
    git clone https://github.com/lllyasviel/Fooocus.git /tmp/Fooocus
    if [ $? -ne 0 ]; then
        echo "Failed to clone Fooocus repository" >&2
        exit 1
    fi
else
    echo "Fooocus repository already exists."
fi

# Start the Flask app (fooocus_server.py)
echo "Starting Fooocus Flask server..."
python3 backend/fooocus_server.py

# Exit with success
exit 0