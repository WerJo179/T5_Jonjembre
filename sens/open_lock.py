#!/usr/bin/env python

import time
import RPi.GPIO as GPIO

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define lock pin
LOCK_PIN = 24

# Set up lock pin as output
GPIO.setup(LOCK_PIN, GPIO.OUT)

try:
    # Activate lock by outputting 5V to LOCK_PIN
    GPIO.output(LOCK_PIN, GPIO.HIGH)
    print("Lock opened.")
    
    # Wait for a short duration
    time.sleep(2)

    # Deactivate lock
    GPIO.output(LOCK_PIN, GPIO.LOW)
    print("Lock closed.")

finally:
    # Clean up GPIO settings
    GPIO.cleanup()
