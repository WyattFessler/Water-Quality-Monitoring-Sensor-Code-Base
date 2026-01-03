#This script will monitor the UDP connection between the PI zeros and the control pi3

import RPi.GPIO as GPIO
import os
import time
#import the necessary libraries

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
#initialize the necessary GPIOs

pi_zero_ips = ["192.168.7.2", "192.168.8.2", "192.168.9.2"]
#IP addresses of the destinations (each pi zero)

#Main loop: Check if each ping results in a response. Send output to GPIO that corresonds 
#true or false. This will be read by the operator as an LED signal
try:
    while True: #continous loop while script is running
        all_connected = True #define variable of connection as true initially
        for ip in pi_zero_ips: #ping each pi zero (IP addresses defined in "pi_zero_ips")
            response = os.system("ping -c 1 -W 1" + ip + " > /dev/null 2>&1")
            
            #for trouble shooting: print statement if ONE or MORE pi zeros are not reachable
            if response != 0: 
                all_connected = False
                print("Pi Zero at" + ip + "NOT reachable")
            else:
                print("Pi Zero at" + ip+ "reachable.")
        
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