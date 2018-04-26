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
        # self.request is the TCP socket object connected to the client.
        self.data = self.request.recv(4096).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # upper-case it and send it back
        self.request.sendall(self.data.upper())


class ServerMain(socketserver.TCPServer):
    def service_actions(self):
        log.dbg("serve_forever called successfully.")
        # there should be code to do something like shoot back
        # some sensor data from the on-board arduino here.
        # except there isn't. oops.

    def server_close(self):
        log.wng("Cleaning up...")
        # put some cleanup stuff here. probably tie up GPIO, etc etc.
        log.wng("Stopping!")
        log.showcounters()


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # start background subprocess for streaming out main camera interface
    subprocess.run("raspivid -o - -t 0 -n -w 1280 -h 720 -fps 30 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp:"
                   "//:8554/}' :demux=h264", shell=True)

    with ServerMain((HOST, PORT), ServerHandler) as server:
        server.serve_forever()