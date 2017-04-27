import select
import socket
import sys
import threading


stop_loop = False

def read_thread(port):
    # A lot of error handling elided.
    sock = socket.socket()
    # We connect in blocking just for simplicity.
    sock.connect(("localhost", port))
    sock.setblocking(False)

    try:
        while not stop_loop:
            ready_set, _, _ = select.select([sock], [], [])
            if not ready_set:
                return
            else:
                data = sock.recv(1024)
                print "Received data:", data
    except Exception as e:
        print e
    finally:
        sock.setblocking(True)
        sock.close()

def run(port):
    """Tries to read from a server connected to port."""
    global stop_loop
    t = threading.Thread(target=read_thread, args=(port,))
    print "Program is running. Press any key to quit."
    t.start()
    raw_input()
    stop_loop = True
    t.join()


if __name__ == "__main__":
    run(int(sys.argv[1]))
