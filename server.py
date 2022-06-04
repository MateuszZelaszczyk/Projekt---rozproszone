from _thread import *
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