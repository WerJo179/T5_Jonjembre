#!/usr/bin/env python

import os
import time
import RPi.GPIO as GPIO
import boto3
import mimetypes

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define sensor pin
SENSOR_PIN = 18

# Set up sensor pin
GPIO.setup(SENSOR_PIN, GPIO.IN)

# S3 bucket configuration
bucket_name = "t5jonjembre"
s3_client = boto3.client('s3')

# Flag to track door state and image capture
door_open = False
image_captured = False

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

# Function to upload image to S3
def upload_image_to_s3(image_filename):
    try:
        mime_type, _ = mimetypes.guess_type(image_filename)
        if mime_type:
            extra_args = {'ContentType': mime_type}
        else:
            extra_args = {}
        with open(image_filename, 'rb') as f:
            s3_client.upload_fileobj(f, bucket_name, f"captured_images/{os.path.basename(image_filename)}", ExtraArgs=extra_args)
        print(f"Image '{image_filename}' uploaded to S3 bucket '{bucket_name}/captured_images' successfully.")
    except Exception as e:
        print(f"Failed to upload image '{image_filename}' to S3 bucket '{bucket_name}/captured_images': {e}")

# Function to log door activity
def log_door_activity(activity):
    ensure_log_file_exists()  # Ensure log file exists
    entry_log = f"{activity}: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    with open("/home/pi/T5_Jonjembre/entry.txt", "a") as f:
        f.write(entry_log)
    # Upload log file to S3
    try:
        s3_client.upload_file("/home/pi/T5_Jonjembre/entry.txt", bucket_name, "logs/entry.txt")
        print(f"Log file 'entry.txt' uploaded to S3 bucket '{bucket_name}/logs' successfully.")
    except Exception as e:
        print(f"Failed to upload log file 'entry.txt' to S3 bucket '{bucket_name}/logs': {e}")

# Function to ensure log file exists
def ensure_log_file_exists():
    log_file_path = "/home/pi/T5_Jonjembre/entry.txt"
    if not os.path.exists(log_file_path):
        with open(log_file_path, "w"):
            pass

# Read voltage of GPIO18 and capture image if voltage is 1
try:
    image_captured = 0 # Initializing variable for image capture
    while True:
        voltage = GPIO.input(SENSOR_PIN)

        if voltage == 1:
            if not door_open:  # Door opened
                door_open = True
                if image_captured == 0:  # Capture image only once when door is opened
                    ensure_img_folder_exists()
                    next_image_filename = get_next_image_filename()
                    os.system(f"libcamera-jpeg -n -o {next_image_filename} > /dev/null 2>&1")
                    upload_image_to_s3(next_image_filename)
                    os.remove(next_image_filename)  # Remove local image after upload to save space
                    image_captured = 1 # Set image variable to 1 (image took)
                log_door_activity("Door opened")
        else:
            if door_open:  # Door closed
                door_open = False
                image_captured = 0 # Reset image variable to 0
                log_door_activity("Door closed")

        time.sleep(0.5)  # Sleep for 0.5 seconds (half a second)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
