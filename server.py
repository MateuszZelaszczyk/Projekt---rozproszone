from _thread import *
import socket
from map import Map


class Server:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.map = Map(600, 700)
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

    def read_pos(self, str):
        str = str.split(",")
        return int(str[0]), int(str[1])

    def make_pos(self, tup):
        return str(tup[0]) + "," + str(tup[1])

    def threaded_client(self, connect, player):
        pos = [(0, 0), (100, 100)]
        messgage = self.make_pos(pos[player]) + ";" + self.map.get_objects_coordinates_as_str()
        connect.send(str.encode(messgage))
        print("Sending: ", messgage)
        reply = ""
        while True:
            try:
                data = connect.recv(2048).decode()
                if not data:
                    print("Disconnected")
                    break
                else:
                    print("Recieved:", data)
                    pos[player], eaten_plants = self.read_positions(data)
                    print('internal data')
                    print(eaten_plants)
                    self.map.delete_objects(eaten_plants)
                    if player == 1:
                        self.player1_eaten_plants = eaten_plants
                        reply = self.make_pos(pos[0]) + ";" + self.make_player2_plants()
                        self.player2_eaten_plants.clear()
                    else:
                        self.player2_eaten_plants = eaten_plants
                        reply = self.make_pos(pos[1]) + ";" + self.make_player1_plants()
                        self.player1_eaten_plants.clear()

                    print("Sending: ", reply)
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