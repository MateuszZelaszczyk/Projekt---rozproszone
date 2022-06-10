from _thread import *
import socket
from map import Map
import sys
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
server = ip
port = 5555
map1 = Map(600, 700)
map2 = Map(600, 700)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
s.listen(2)
print("Waiting for a connection, Server Started")


def read_pos(pos_str):
    pos_str = pos_str.split(",")
    return str(pos_str[0]), int(pos_str[1]), int(pos_str[2])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2])

def get_map_for_position(pos):
    if pos[0] == 'm1':
        return map1
    return map2

pos = [('m1', 0, 0), ('m1', 100, 100)]


def threaded_client(connect, player):
    connect.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(connect.recv(2048).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    position_to_send = pos[0]
                else:
                    position_to_send = pos[1]
                map = get_map_for_position(position_to_send)
                reply = make_pos(position_to_send) + ";" + map.get_objects_coordinates_as_str()
                print("Recieved:", data)
                print("Sending: ", reply)
            connect.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    connect.close()


currentPlayer = 0
while True:
    connect, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (connect, currentPlayer))
    currentPlayer += 1
