import service
import socket
from threading import Thread


HOST = 'localhost'
PORT = 8000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(5)

class Server:
    def __init__(self):
        self.clients = {}
        service.start_cervices()

    def listen(self, port, ClientClass):
        print('Server started on port <{}>'.format(port))
        try:
            while True:
                conn, addr = sock.accept()
                client = ClientClass(conn, addr)
                th = Thread(target=client.loop)
                th.daemon = True
                th.start()
        except KeyboardInterrupt:
            print('Server stopped')
            pass

    def connect(self, client):
        self.clients[client.uid] = client
        print('Client connectd {}'.format(client))

    def recv(self, client, msg, args):
        print('Message from {}: {}'.format(client, msg))

server = Server()
