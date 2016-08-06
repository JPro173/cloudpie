import service
from time import sleep


class Server():
    def __init__(self):
        self.clients = {}
        service.start_cervices()

    def listen(self, port):
        print('Server started on port <{}>'.format(port))
        try:
            sleep(10000)
        except KeyboardInterrupt:
            print('Server stopped')
            pass

    def connect(self, client):
        self.clients[client.uid] = client
        print('Client connectd {}'.format(client))

    def recv(self, client, msg, args):
        print('Message from {}: {}'.format(client, msg))

server = Server()
