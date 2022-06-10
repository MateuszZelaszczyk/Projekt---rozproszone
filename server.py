from _thread import *
import socket
from map import Map


class Server:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.player1_points = 0
        self.player2_points = 0
        self.port = 5555
        self.player_positions = [('m1', 0, 0), ('m1', 200, 200)]
        self.map = Map(600, 700)
        #self.map2 = Map(600, 700)
        self.player1_eaten_plants = []
        self.player2_eaten_plants = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.init_listener()

    def init_listener(self):
        try:
            self.socket.bind((self.ip, self.port))
        except socket.error as e:
            str(e)
        self.socket.listen(2)
        print("Waiting for a connection, Server Started")

    def make_player1_plants(self):
        return ','.join([str(key) for key in self.player1_eaten_plants])

    def make_player2_plants(self):
        return ','.join([str(key) for key in self.player2_eaten_plants])

    def read_positions(self, data):
        data = data.split(";")
        player_pos = self.read_pos(data[0])
        data.pop(0)
        data = data[0].split(",")
        if data[0] != '':
            eaten_plants = [int(key) for key in data]
        else:
            eaten_plants = []
        return player_pos, eaten_plants

    def read_pos(self, pos_str):
        pos_str = pos_str.split(",")
        return str(pos_str[0]), int(pos_str[1]), int(pos_str[2])

    def make_pos(self, tup):
        return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2])

    def threaded_client(self, connect, player):
        messgage = self.make_pos(self.player_positions[player]) + ";" + self.map.get_objects_coordinates_as_str()
        connect.send(str.encode(messgage))
        #print("Sending: ", messgage)
        while True:
            try:
                data = connect.recv(2048).decode()
                if not data:
                    print("Disconnected")
                    break
                else:
                    self.player_positions[player], eaten_plants = self.read_positions(data)
                    self.map.delete_objects(eaten_plants)
                    if player == 1:
                        self.player1_points += len(eaten_plants)
                        self.player1_eaten_plants = eaten_plants
                        #map = self.get_map_for_position(self.player_positions[0])
                        reply = self.make_pos(self.player_positions[0]) + ";" + self.make_player2_plants()
                        self.player2_eaten_plants.clear()
                    else:
                        self.player2_points += len(eaten_plants)
                        self.player2_eaten_plants = eaten_plants
                        reply = self.make_pos(self.player_positions[1]) + ";" + self.make_player1_plants()
                        self.player1_eaten_plants.clear()
                    #print("Recieved:", data)
                    #print("Sending: ", reply)
                    connect.sendall(str.encode(reply))
            except:
                break
        print("Lost connection")
        connect.close()


server = Server()
current_player = 0
while True:
    connect, address = server.socket.accept()
    print("Connected to:", address)
    start_new_thread(server.threaded_client, (connect, current_player))
    current_player += 1