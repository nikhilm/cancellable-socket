import select
import socket
import sys
import threading


def read_thread(port, notify):
    # A lot of error handling elided.
    sock = socket.socket()
    # We connect in blocking just for simplicity.
    sock.connect(("localhost", port))
    sock.setblocking(False)

    try:
        while True:
            ready_set, _, _ = select.select([sock, notify], [], [])
            if not ready_set:
                return
            elif ready_set[0] == notify:
                print "User requested cancellation"
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
    cancel, notify = socket.socketpair()
    t = threading.Thread(target=read_thread, args=(port, notify))
    print "Program is running. Press any key to quit."
    t.start()
    raw_input()
    cancel.close()
    t.join()


if __name__ == "__main__":
    run(int(sys.argv[1]))
