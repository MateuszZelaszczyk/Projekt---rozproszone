from _thread import *
from distutils.log import error
import  socket
import sys
 
server = "192.168.1.198"
port = 5555

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

def threaded_client(connect):
    reply=""
    while True:
        try:
            data = connect.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Recieved:", reply)
                print("Sending: ", reply)
            connect.sendall(str.encode(reply))
        except:
            break

while True:
    connect, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (connect,) )