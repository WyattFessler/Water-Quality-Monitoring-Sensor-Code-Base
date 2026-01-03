# This code will periodically send a "trigger" to the pi zero, which will be recieved by the 
# capture server and prompt an image to be taken

import socket
import time
#import the necessary libraries

# Target configuration: tuples of usb port and im address that the pi3 will see for each pi zero
targets = [
    ("192.168.7.2", "usb0"),
    ("192.168.8.2", "usb1"),
    ("192.168.9.2", "usb2")
]

PORT = 5005
PORT_TIME = 5004
TRIGGER_MESSAGE = "TRIGGER"
#define the port and time as the same as in the capture server. Message "trigger" just for 
# troubleshooting purposes

#defines a function that sends the trigger to the pi zero
def send_trigger(target_ip, interface_name):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to specific interface (SO_BINDTODEVICE)
    sock.setsockopt(socket.SOL_SOCKET, 25, interface_name.encode())
    sock.sendto(TRIGGER_MESSAGE, (target_ip, PORT)) #sends the trigger message
    sock.close() #closes the connection

#defines a function that will send the time of the pi3 to each zero to synchornize
def send_time(target_ip, interface_name):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #gets the current time of the pi3
    message = now.encode() #encodes the time to be sent
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, 25, interface_name.encode())
    sock.sendto(message, (target_ip, PORT_TIME)) #sends the time to the capture server
    sock.close()

#Main loop: Runs the trigger and time send every 2 seconds
while True:
    for target_ip, interface_name in targets: #runs loop for each IP and Interface name sequentially (not technically synchronized)
        print("Sending trigger to" + target_ip+  "via interface}" + {interface_name})
        try: #attempt to send trigger and time to each pi zero
            send_trigger(target_ip, interface_name) 
            send_time(target_ip, interface_name)
        except:
            print("Failed to send to" + {target_ip})
    time.sleep(2) #wait 2 seconds to repeat (camera initialization time)