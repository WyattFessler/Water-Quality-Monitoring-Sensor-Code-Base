import RPi.GPIO as GPIO
import os
import time

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

# List of Pi Zero IPs
pi_zero_ips = ["192.168.7.2", "192.168.8.2", "192.168.9.2"]

try:
    while True:
        all_connected = True
        for ip in pi_zero_ips:
            response = os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1")
            if response != 0:
                all_connected = False
                print(f"Pi Zero at {ip} NOT reachable.")
            else:
                print(f"Pi Zero at {ip} reachable.")
        
        # If all are connected, flash LED once
        if all_connected:
            GPIO.output(18, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(18, GPIO.LOW)
        else:
            # If one or more are not connected, blink rapidly
            for _ in range(3):
                GPIO.output(18, GPIO.HIGH)
                time.sleep(0.1)
                GPIO.output(18, GPIO.LOW)
                time.sleep(0.1)
        
        time.sleep(5)  # Wait 5 seconds before next check

finally:
    GPIO.cleanup()