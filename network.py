import socket
import pickle

class Network:
    def __init__(self):
        # Initialize network-related variables
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket for the client
        #self.server = "127.0.0.1"  # Server IP for local testing
        self.server = "10.6.8.167" # Server IP address
        self.port = 5555  # Port number for communication
        self.addr = (self.server, self.port)  # Server address and port
        self.p = self.connect()  # Connect to the server and retrieve initial data (player object)

    def getP(self):
        return self.p

    def connect(self):
        try:
            # Attempt to connect to the server
            self.client.connect(self.addr)
            # Receive initial data (player object) from the server after connection
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, msgtype, data):
        try:
            # Send msgtype and data to the server and return it to the client

            message = (msgtype, data)
            self.client.send(pickle.dumps(message))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
