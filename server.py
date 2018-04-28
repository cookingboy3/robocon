# robocon server
# main class
import lumberjack
import socketserver
import json
import subprocess
import pigpio

# configuration variables
logginglevel = 2  # loglevel passed
log = lumberjack.Lumberjack("server.py", "MAIN", logginglevel)  # global lumberjack

pwmhell = pigpio.pi()

# Variable Hell
js_throttle = 50
js_pitch = 50
js_yaw = 50
js_roll = 50
claw_state = False

claw_last_state = False

key_kill = False

class ServerHandler(socketserver.BaseRequestHandler):
    """
    Request handler class
    """

    def map(x, in_min, in_max, out_min, out_max):
        return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

    def drivePain():
        # Check if claw has changed
        if claw_state != claw_last_state:
            # Move the claw
            if claw_state == False:
                # Close claw
                #servoActuate(?, 100)
                claw_last_state = True
            else:
                #Open claw
                #servoActuate(?, 0)
                claw_last_state = False
        # Forward/backward motor

        # Up/down motor

    def servoActuate(channel, target):
        if channel == 999 or 998 or 997:
            # Use specific range for channel
            pwmhell.set_servo_pulsewidth(channel, map(target, 0, 100, 1100, 1900))
        else:
            # Use full range
            pwmhell.set_servo_pulsewidth(channel, map(target, 0, 100, 1100, 1900))

    def handle(self):
        try:
            client_ip = str(self.client_address[0])

            while 1:
                try:
                    self.data = self.request.recv(4096).decode("utf-8").strip()
                    print("{} wrote:".format(self.client_address[0]))
                    print(self.data)
                    try:
                        jsondata = json.loads('{' + self.data + '}')
                        log.dbg(jsondata["message_type"])
                        log.dbg(jsondata["stick_roll"])
                        log.dbg(jsondata["stick_yaw"])
                        log.dbg(jsondata["stick_pitch"])
                        log.dbg(jsondata["stick_throttle"])
                        if jsondata["message_type"] == "STICK_UPDATE":
                            log.dbg("looks like a stick update message boss")
                    except Exception as ex:
                        log.err("oh shit")
                        log.err(ex)
                except KeyboardInterrupt:
                    key_kill = True
                    break
        except:
            pass
        if key_kill == False:
            log.wng('Client %s decided it was time to go. Bye.' % str(self.client_address[0]))

class ServerMain(socketserver.TCPServer):
    # def service_actions(self):
        # log.dbg("serve_forever called successfully.")
        # there should be code to do something like shoot back
        # some sensor data from the on-board arduino here.
        # except there isn't. oops.


    def server_close(self):
        log.wng("Cleaning up...")
        # put some cleanup stuff here. probably tie up GPIO, etc etc.
        log.wng("Stopping!")
        log.showcounters()


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999

    # start background subprocess for streaming out main camera interface

    #subprocess.Popen("raspivid -o - -t 0 -n -w 1280 -h 720 -fps 30 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp:"
    #               "//:8554/}' :demux=h264", shell=True)
    #subprocess.Popen(["gst-launch-1.0 rpicamsrc preview=false ! 'video/x-h264, width=1280, height=720"
    #                   "framerate=30/1,profile=high' ! queue ! rtph264pay ! udpsink host=10.4.10.131 port=5000"], shell=True)

    with ServerMain((HOST, PORT), ServerHandler) as server:
        server.serve_forever()
