import socket
import SocketServer
import sys
import time

class WaitAndWrite(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            while True:
                time.sleep(5)
                self.request.sendall("hello world")
        except socket.error:
            print "client disconnected"

def run(port):
    server = SocketServer.TCPServer(("localhost", port), WaitAndWrite)
    server.serve_forever()

if __name__ == "__main__":
    run(int(sys.argv[1]))
