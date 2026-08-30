#!/bin/bash

# GitHub repository URL
REPO_URL="https://github.com/shuck-hh/heindl-node-red.git"

# Working directory
WORK_DIR="/home/node/heindl-node-red"
cd "$WORK_DIR" || exit 1

# Check whether the machine has internet access before fetching updates
if ! curl -fsSL --max-time 5 https://github.com >/dev/null 2>&1; then
    echo "No internet connection detected. Skipping update."
    exit 0
fi

# Fetch the latest information from GitHub
git fetch origin -q

# Check whether the local working tree differs from origin
if ! git diff --quiet HEAD origin/HEAD; then
    echo "Changes detected compared to GitHub."
    echo "Updating..."

    # Stopping the services that get an update
    echo "Stopping relevant services..."
    sudo systemctl stop cpp.service
    sudo systemctl stop py.service

    # Delete the clone
    cd ~
    sudo rm -r -f heindl-node-red

    # Clone again
    git clone "$REPO_URL" -q

    # Re-install the services
    echo "Reinstalling services..."
    cd heindl-node-red/autostart/
    bash install.sh

    echo "Update done."

    # Reboot (disabled because of possible restart loop)
    # echo "Rebooting..."
    # sudo reboot
else
    echo "No changes detected."
    exit 0
fi
