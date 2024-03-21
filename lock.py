#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define buzzer and lock pins
BUZZER_PIN = 17
LOCK_PIN = 24

# Set up buzzer and lock pins
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(LOCK_PIN, GPIO.OUT)

# Create PWM instance for the buzzer
pwm = GPIO.PWM(BUZZER_PIN, 1000)  # 1000 Hz frequency

# Create an object of the class MFRC522
reader = SimpleMFRC522()

# Allowed NFC card IDs
allowed_ids = ['975827638292', '702062598653', '700636469675']

# Welcome message
print("Looking for card")
print("Press Ctrl-C to stop")

# This loop checks for tags.
try:
    while True:
        reader = SimpleMFRC522()
        id, text = reader.read()
        print("NFC Card ID:", id)
        print("NFC Card Text:", text)

        # Convert card ID to string for comparison
        card_id_str = str(id)

        # Check if the card ID is allowed
        if card_id_str in allowed_ids:
            print("Access granted")

            # Activate lock by outputting 3.3V to LOCK_PIN
            GPIO.output(LOCK_PIN, GPIO.HIGH)

            # Play buzzer sound with PWM
            pwm.start(50)  # Start PWM with 50% duty cycle (moderate tone)
            time.sleep(1)  # Play sound for 2 seconds
            pwm.stop()  # Stop PWM

            # Deactivate lock
            GPIO.output(LOCK_PIN, GPIO.LOW)

        else:
            print("Access denied")

            # Beep the buzzer 3 times for access denied
            pwm.start(50) # PWM with 50% duty cycle
            for _ in range(3):
                time.sleep(0.2)  # Beep duration
                pwm.stop()  # Stop PWM
                time.sleep(0.2)  # Silence duration
                pwm.start(50)  # Resume PWM
            pwm.stop()  # Stop PWM

        time.sleep(5)  # Wait for 5 seconds before scanning again
        pwm.start(50)
        time.sleep(0.1)
        pwm.stop()
except KeyboardInterrupt:
    print("Exiting...")
finally:
    pwm.stop()  # Stop PWM
    GPIO.cleanup()
