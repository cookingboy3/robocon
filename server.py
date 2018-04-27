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
                self.data = self.request.recv(1024)
                if not self.data:
                    break

                received_data = self.data.decode('utf-8').strip()

                # print debug
                print("%s wrote: %s" % (client_ip, received_data))

                # respond
                self.request.send(received_data.upper().encode('utf-8'))
        except:
            pass

        print('Client %s decided it was time to go.' % str(self.client_address[0]))

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
    HOST, PORT = "localhost", 9999

    # start background subprocess for streaming out main camera interface
    subprocess.run("raspivid -o - -t 0 -n -w 1280 -h 720 -fps 30 | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp:"
                   "//:8554/}' :demux=h264", shell=True)

    with ServerMain((HOST, PORT), ServerHandler) as server:
        server.serve_forever()
