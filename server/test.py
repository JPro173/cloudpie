import time

import service

from threading import Thread


HOST = 'localhost'

class Server:
    def __init__(self):
        self.clients = {}
        service.start_cervices()
        #start clients
        time.sleep(3000)

    def connect(self, client):
        self.clients[client.uid] = client
        print('Client connectd {}'.format(client))

    def recv(self, client, msg, args):
        print('Message from {}: {}'.format(client, msg))

server = Server()
