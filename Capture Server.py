# This script will establish a UDP connection over the wired USB connection between the 
# PI zero (in gadget mode) and the pi3. It will then take images when triggered and send
# them to the pi3

import socket
from picamera2 import Picamera2
import time
import subprocess
import os
#import necessary libraries 

Picamera2.start() #initialize the Arducam via picamera

UDP_IP = "192.168.7.2" 
UDP_PORT = 5005
PORT_TIME = 5004
#Define UDP connection IP (IP of pi zero, which is specific to each device)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
#Define the socket and attempt to bind using the IP and Port

sock_time = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_time.bind((UDP_IP, PORT_TIME))

PI3_USER = "underdac-pi3"
PI3_IP = "192.168.7.1" # IP of recieving end (applicable port of PI3B+)
PI3_DEST_DIR = "/media/underdac-pi3/UNDERDAC/zero1"
#Define the deistnation (User of PI3, IP of PI3, and directory where the images will be saved)

# BELOW: Main loop. Will synchormized time, look for trigger from pi3, take images, and send them
while True: 
    try: #attempt to get the time from the pi3 to synchronize each PI zero
        data, addr = sock_time.recvfrom(1024)
        timestamp = data.decode()
        print("recieved")
        print (timestamp)
        subprocess.run(["sudo", "date", "-u", "-d", f"@{timestamp}"]) # set time to match the recieved timestamp
    except socket.timeout:
        pass

    data, addr = sock.recvfrom(1024)
    print("Trigger received from", addr)
    #Look for trigger received from the PI3

    filename = "/home/underdac-zero1/capture_" + {timestamp}+ ".jpg" #names image as the date/time
    Picamera2.capture_file(filename) #capture image

    print("Image saved")
    TIME = time.time() #time stamp for troubleshooting
    print(TIME)

    # SCP the image to Pi 3
    scp_cmd = ["scp", filename, f"{PI3_USER}@{PI3_IP}:{PI3_DEST_DIR}/"] #command to SCP image in terminal
    try:
        subprocess.run(scp_cmd, check=True)
        print(f"Image successfully copied to {PI3_IP}:{PI3_DEST_DIR}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to copy image: {e}")