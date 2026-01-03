#This script monitor whether or not the USB connected SSD harddrive is being recognized by the sensor. 
#This gives an LED output that can be read by the user before deployment of the sensor

import RPi.GPIO as GPIO
import time
import os
#import the necessary libraries

MOUNT_POINT = "/media/pi/USBDRIVE"
MOUNTED_LED_GPIO = 22
UNMOUNTED_LED_GPIO = 27
#determine USB connection location and set output pin variables

# Setup GPIO in Raspberry PI
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOUNTED_LED_GPIO, GPIO.OUT)
GPIO.setup(UNMOUNTED_LED_GPIO, GPIO.OUT)

def is_mounted(mount_point):
    return os.path.ismount(mount_point)
#define a function to determine if mountpoint is operational

try: #check if USB is mounted continously. If mounted, pin 22 is powered (LED illuminated) if not, 27 is powered (other LED illuminated)
    print("Starting USB monitor...")
    while True:
        if is_mounted(MOUNT_POINT):
            GPIO.output(MOUNTED_LED_GPIO, GPIO.HIGH)
            GPIO.output(UNMOUNTED_LED_GPIO, GPIO.LOW)
        else:
            GPIO.output(MOUNTED_LED_GPIO, GPIO.LOW)
            GPIO.output(UNMOUNTED_LED_GPIO, GPIO.HIGH)
        time.sleep(1)  
except KeyboardInterrupt: #cancel operation option if user is in control, not necessary for sensor operation
    print("Exiting...")
finally:
    GPIO.cleanup()