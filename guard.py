#!/usr/bin/env python

import os
import time
import RPi.GPIO as GPIO

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define sensor pin
SENSOR_PIN = 18

# Set up sensor pin
GPIO.setup(SENSOR_PIN, GPIO.IN)

# Function to check if the img folder exists and create it if not
def ensure_img_folder_exists():
    img_folder = "/home/pi/T5_Jonjembre/img"
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

# Function to get the image file name with timestamp
def get_next_image_filename():
    current_time = time.strftime("%d-%m-%Y-%H:%M:%S")
    filename = f"/home/pi/T5_Jonjembre/img/{current_time}.jpg"
    return filename

# Read voltage of GPIO18 and capture image if voltage is 1
try:
    while True:
        voltage = GPIO.input(SENSOR_PIN)
        
        if voltage == 1:
            next_image_filename = get_next_image_filename()
            os.system(f"libcamera-jpeg -n -o {next_image_filename} > /dev/null 2>&1")

        time.sleep(0.5)  # Sleep for 0.5 seconds (half a second)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
