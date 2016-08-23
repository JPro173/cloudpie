import service

from fake_client import FakeClient


def tests(*scenes):
    clients = [FakeClient(scen) for scen in scenes]

    for i in range(200):
        for client in clients:
            client.step(i)

class Server:
    def __init__(self):
        self.clients = {}
        service.start_cervices()

        tests(
            'user00',
            'user01',
            'cant_login'
        )
        print('Tests passed')

    def recv(self, client, msg, args):
        print('Message from {}: {}'.format(client, msg))

server = Server()
