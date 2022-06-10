from _thread import *
import  socket
import sys

def is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

SERVER_PORTS = [6666, 6667]

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
server = ip
port = 5555

scom_port = None
for p in SERVER_PORTS:
    print("Now checking port ", p)
    if not is_port_in_use(p):
        scom_port = p
        break
    else:
        print (f"port {p} is in use on this server")

if(scom_port == None):
    print("All server ports are occupied. Cannot start server.")
    exit(1)
else:
    print(f"SCOM port for this server is {scom_port}")

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("sth else")
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

def read_pos(str):
    str=str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])
    
pos=[(0,0),(100,100)]

def threaded_client(connect, player):
    connect.send(str.encode(make_pos(pos[player])))
    reply=""
    while True:
        try:
            data = read_pos(connect.recv(2048).decode())
            pos[player] = data
            
            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Recieved:", data)
                print("Sending: ", reply)
            connect.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Lost connection")
    connect.close()

currentPlayer =0
while True:
    connect, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (connect, currentPlayer) )
    currentPlayer +=1