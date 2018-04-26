# robocon client
# main
import socket
import sys
import lumberjack
import pygame
import sys

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])
log = lumberjack.Lumberjack("client.py", "CLIENT", 2)

# joystick init and setup and stuff
log.dbg("Starting joystick init")
pygame.init()
pygame.joystick.init()
if pygame.joystick.get_count() < 1 or pygame.joystick.get_count() > 1:
    log.err(f"Found {pygame.joystick.get_count()} joysticks. Ensure only one is plugged in!")
    log.err(f"Joystick find and connect failed. Stopping!")
    pygame.quit()
    sys.exit(1)


# create a TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # connect and send data
    sock.connect((HOST,PORT))
    sock.sendall(bytes(data + "\n", "utf-8"))

    received = str(sock.recv(4096), "utf-8")