# robocon server
# main class
import lumberjack
import socketserver
import json
import subprocess

# configuration variables
logginglevel = 2  # loglevel passed
log = lumberjack.Lumberjack("server.py", "MAIN", logginglevel)  # global lumberjack


class ServerHandler(socketserver.BaseRequestHandler):
    """
    Request handler class
    """

    def handle(self):
        try:
            client_ip = str(self.client_address[0])

            while 1:
                self.data = self.request.recv(4096).decode("utf-8").strip()
                print("{} wrote:".format(self.client_address[0]))
                print(self.data)
                try:
                    jsondata = json.loads(self.data)
                    if jsondata["message_type"] == "STICK_UPDATE":
                        log.dbg("looks like a stick update message boss")
                except Exception as ex:
                    log.err("oh shit")
                    log.err(ex)
        except:
            pass

        log.wng('Client %s decided it was time to go.' % str(self.client_address[0]))

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
