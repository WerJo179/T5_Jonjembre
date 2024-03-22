Description:
This repository contains the files used for my project for school, in combination with a RPi.

Contents:
Scripts: Contains the Python scripts used in the project.
Documentation: Includes any relevant documentation or notes about the project.

Getting Started:
To get started with this project, please read carefully through the instructions.

After deployment:
After you followed all the steps from our instructions, the scripts should work automatically
upon rebooting the device.

We have 2 additional scripts that you can run manually from the terminal if needed.

open_lock.py : This script will open up the lock from the cabinet.
This is required if you don't have access to your cards and you need to open the cabinet manually.
IMPORTANT: After using this script manually, please reboot your device. The other scripts stop working
after using this, rebooting solves that.

read.py : This script will read your cards using the RFID Reader and print out the ID attached to the card,
aswell as the text if the card has one assigned. Useful if you wish to see the ID to use it for whatever case.
