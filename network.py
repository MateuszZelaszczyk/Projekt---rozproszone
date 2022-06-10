from cmath import exp
import  socket
from unittest import expectedFailure

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

    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(4096).decode()
        except:
            pass
    def send(self,data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(4096).decode()
        except socket.error as e:
            print(e)

