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

# Constant pls
unnamed_one = 2
unnamed_two = 3
unnamed_three = 4
unnamed_four = 17
claw_servo_gpio = 27
unnamed_six = 22

# Variable Hell
js_throttle = 50.0
js_pitch = 50.0
js_yaw = 50.0
js_roll = 50.0
claw_state = False

claw_last_state = False

key_kill = False

class ServerHandler(socketserver.BaseRequestHandler):
    """
    Request handler class
    """

    def notmap(self, x, in_min, in_max, out_min, out_max):
        try:
            log.dbg(x)
        except Exception as e:
            log.err("section kwfw")
            log.err(e)
        try:
            log.dbg(((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min))
        except Exception as e:
            log.err("section mwfw")
            log.err(e)
        return ((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

    def joyPain(self, jsondata):
        try:
            js_throttle = self.notmap(jsondata["stick_throttle"], -1.0, 1.0, 0.0, 100.0)
            js_pitch = self.notmap(jsondata["stick_pitch"], -1.0, 1.0, 0.0, 100.0)
            js_yaw = self.notmap(jsondata["stick_yaw"], -1.0, 1.0, 0.0, 100.0)
            js_roll = self.notmap(jsondata["stick_roll"], -1.0, 1.0, 0.0, 100.0)
            log.dbg(type(jsondata["stick_throttle"]))
            self.drivePain()
        except Exception as e:
            log.err("section djfjfj")
            log.err(e)

    def drivePain(self):
        # Check if claw has changed
        #if claw_state != claw_last_state:
            # Move the claw
        #    if claw_state == False:
                # Close claw
        #        self.servoActuate(27, 100)
        #        claw_last_state = True
        #    else:
                #Open claw
        #        self.servoActuate(27, 0)
        #        claw_last_state = False
        # go up
        try:
            self.servoActuate(4,  js_throttle)
            self.servoActuate(17, js_throttle)
        except Exception as e:
            log.err("failed up")
            log.err(e)
        # go forward
        #servoActuate(2, js_pitch)
        #servoActuate(3, js_pitch)
        # S P I N
        try:
            self.servoActuate(2,  js_yaw + js_pitch)
            self.servoActuate(3, -js_yaw + js_pitch)
        except Exception as e:
            log.err("failed spin")
            log.err(e)

    def servoActuate(self, channel, target):
        #try:
            #pwmhell.set_servo_pulsewidth(channel, self.notmap(target, 0, 100, 1100, 1900))
        #except Exception as e:
            #log.err(e)
        log.dbg(target)
        log.dbg(self.notmap(target, 0, 100, 1100, 1900))

    def handle(self):
        try:
            client_ip = str(self.client_address[0])
            key_kill = False

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
                        self.joyPain(jsondata)
                    except Exception as e:
                        log.err("uh oh")
                        log.err(e)
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
    HOST, PORT = "0.0.0.0", 9993

    # start background subprocess for streaming out main camera interface

    #subprocess.Popen("raspivid -o - -t 0 -n -w 1280 -h 720 -fps 30 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp:"
    #               "//:8554/}' :demux=h264", shell=True)
    #subprocess.Popen(["gst-launch-1.0 rpicamsrc preview=false ! 'video/x-h264, width=1280, height=720"
    #                   "framerate=30/1,profile=high' ! queue ! rtph264pay ! udpsink host=10.4.10.131 port=5000"], shell=True)

    with ServerMain((HOST, PORT), ServerHandler) as server:
        server.serve_forever()
