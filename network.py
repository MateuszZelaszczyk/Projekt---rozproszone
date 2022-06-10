import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ##< TODO: this should be an individual class as in prodaction this wold be a fixed address, not docker
        hostname = socket.gethostname()
        self.server = socket.gethostbyname(hostname)
        self.port = 5555
        #self.second_server_port = 5556
        ##< TODO
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def get_position(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            reply = self.client.recv(16384).decode()
            return reply
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(4096).decode()
        except socket.error as e:
            print(e)

