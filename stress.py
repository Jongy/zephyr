import socket
import time
import threading

def thread():
    s = socket.create_connection(("192.0.2.1", 4242))

    while True:
        s.send(b"aaaaaaaaaaaaaaaaaaaaaaaaa")
        s.recv(1000)
        print("...")


for i in range(3):
    t = threading.Thread(target=thread)
    t.daemon = True
    t.start()


input("^C to exit...")
