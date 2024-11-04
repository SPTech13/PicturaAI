#!/bin/bash

# Install pygit2
echo "Installing pygit2..."
pip install pygit2==1.15.1

# Clone the Fooocus repository if it doesn't already exist
if [ ! -d "/tmp/Fooocus" ]; then
    echo "Cloning Fooocus repository..."
    git clone https://github.com/lllyasviel/Fooocus.git /tmp/Fooocus
else
    echo "Fooocus repository already exists."
fi

# Start the Flask app (fooocus_server.py)
echo "Starting Fooocus Flask server..."
python fooocus_server.py
