#!/bin/bash

# Update package lists and upgrade installed packages
sudo apt update && sudo apt upgrade -y

# Install Python 3, Python 3 development packages, pip, and venv
sudo apt install python3 python3-dev python3-pip python3-venv git -y

# Install necessary Python packages using pip3
sudo pip3 install adafruit-circuitpython-dht RPi.GPIO spidev mfrc522 boto3 -y
