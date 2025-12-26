import socket
from picamera2 import Picamera2
import time
import subprocess
import os

picam2 = Picamera2()
picam2.start()

UDP_IP = "192.168.7.2"
UDP_PORT = 5005
PORT_TIME = 5004

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

sock_time = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_time.bind((UDP_IP, PORT_TIME))

# Set your Pi 3 username, IP, and target folder here
PI3_USER = "underdac-pi3"
PI3_IP = "192.168.7.1"  # Replace with Pi 3 IP address
PI3_DEST_DIR = "/media/underdac-pi3/UNDERDAC/zero1"

while True:
    try:
        data, addr = sock_time.recvfrom(1024)
        timestamp = data.decode()
        print(f"recieved")
        print (timestamp)
        subprocess.run(["sudo", "date", "-u", "-d", f"@{timestamp}"])
    except socket.timeout:
        pass

    data, addr = sock.recvfrom(1024)
    print("Trigger received from", addr)

    filename = f"/home/underdac-zero1/capture_{timestamp}.jpg"
    picam2.capture_file(filename)
    print(f"Image saved to {filename}")
    TIME = time.time()
    print(TIME)
    # SCP the image to Pi 3
    scp_cmd = ["scp", filename, f"{PI3_USER}@{PI3_IP}:{PI3_DEST_DIR}/"]
    try:
        subprocess.run(scp_cmd, check=True)
        print(f"Image successfully copied to {PI3_IP}:{PI3_DEST_DIR}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to copy image: {e}")