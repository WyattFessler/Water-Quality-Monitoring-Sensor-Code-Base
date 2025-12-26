#!/usr/bin/env python3

import socket
import time

# Target configuration: Zero IP, Pi 3 interface
targets = [
    ("192.168.7.2", "usb0"),
    ("192.168.8.2", "usb1"),
    ("192.168.9.2", "usb2")
]

PORT = 5005
PORT_TIME = 5004
TRIGGER_MESSAGE = b"TRIGGER"

def send_trigger(target_ip, interface_name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to specific interface (SO_BINDTODEVICE)
    sock.setsockopt(socket.SOL_SOCKET, 25, interface_name.encode())
    sock.sendto(TRIGGER_MESSAGE, (target_ip, PORT))
    sock.close()

def send_time(target_ip, interface_name):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = now.encode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, 25, interface_name.encode())
    sock.sendto(message, (target_ip, PORT_TIME))
    sock.close()

while True:
    for target_ip, interface_name in targets:
        print(f"Sending trigger to {target_ip} via interface {interface_name}")
        try:
            send_trigger(target_ip, interface_name)
            send_time(target_ip, interface_name)
        except OSError as e:
            print(f"Failed to send to {target_ip} via {interface_name}: {e}")
    time.sleep(2)