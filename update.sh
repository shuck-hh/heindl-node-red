#!/bin/bash

# GitHub repository URL
REPO_URL="https://github.com/USERNAME/REPOSITORY.git"

# Working directory
WORK_DIR="/path/to/your/repository"

cd "$WORK_DIR" || exit 1

# Fetch the latest information from GitHub without changing files
git fetch origin

# Check whether the local working tree differs from origin
if ! git diff --quiet HEAD origin/HEAD; then
    echo "Changes detected compared to GitHub."
    echo "Rebooting..."

    sudo reboot
else
    echo "No changes detected."
fi
