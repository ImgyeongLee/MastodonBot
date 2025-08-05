#!/bin/bash

# Start this bash script for the overall set up
set -e  # Terminate this immediately if an error has been thrown

echo "1. Updating package list..."
sudo apt update

echo "2. Installing software-properties-common..."
sudo apt install -y software-properties-common

echo "3. Adding deadsnakes PPA..."
sudo add-apt-repository -y ppa:deadsnakes/ppa

echo "4. Updating package list again..."
sudo apt update

echo "5. Installing Python 3.11 and development tools..."
sudo apt install -y python3.11 python3.11-venv python3.11-dev

echo "6. Setting Python 3.11 as alternative for python3..."
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

echo "7. Installing tmux..."
sudo apt install -y tmux

echo "✅ All tasks have been completed successfully."
