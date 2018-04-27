# robocon client
# main
import socket
import lumberjack
import pygame
import sys
import json

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])
log = lumberjack.Lumberjack("client.py", "CLIENT", 2)


def sendstickpositionupdate():
    jsondata = '"stick_roll": {0:.3f}, "stick_pitch": {1:.3f}, "stick_yaw": {2:.3f} ' \
               '"stick_throttle": {3:.3f}'.format(stick.get_axis(0), stick.get_axis(1), stick.get_axis(3),
                                                  stick.get_axis(2))
    sock.send(bytes(jsondata + "\n", "utf-8"))

def sendbuttonstateupdate():
    log.wng("button state updated, but I didn't implement. oops.")

# joystick init and setup and stuff
log.dbg("Starting joystick init")
# use the full-fledged pygame.init() call to half-init the video subsystem
# so that the events subsystem will actually work.
pygame.init()
if pygame.joystick.get_count() < 1 or pygame.joystick.get_count() > 1:
    log.err(f"Found {pygame.joystick.get_count()} joysticks. Ensure only one is plugged in!")
    log.err(f"Joystick find and connect failed. Stopping!")
    sys.exit(1)
else:
    log.dbg(f"Found {pygame.joystick.get_count()} joystick successfully.")
log.dbg("Initializing joystick...")
stick = pygame.joystick.Joystick(0)
stick.init()
log.dbg("Joystick correctly initialized, probably.")

# create a TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # connect and send data
    try:
        log.dbg("Trying to connect...")
        sock.connect((HOST,PORT))
    except ConnectionRefusedError:
        log.err("Failed to establish connection to the target. It actively refused it.")
        log.err("Is the target machine running the server?")
        log.err("Stopping!")
        sys.exit(1)

    log.dbg("Connected successfully. Now taking inputs.")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                sendstickpositionupdate()
            if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
                sendbuttonstateupdate()

    # received = str(sock.recv(4096), "utf-8")
