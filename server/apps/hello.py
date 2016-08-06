from service import services
from collections import defaultdict
from apps import BaseApp

class Hello(BaseApp):
    def __init__(self, uid):
        self.admin_uid = uid
        self.clients = defaultdict(list)
        self.a = 0

    def stop(self):
        pass

    def disconnect(self, *args):
        pass

    def connect(self, uid):
        self.clients[uid] = []

    def go(self, n, uid):
        self.clients[uid].append(int(n))
        self.a += int(n)
        return self.a

    def history(self, uid):
        return services['mathe'].protected_join(self.clients[uid], ' ', uid)

    def is_allowed_to_connect(self, permission):
        return True

class HelloService:
    pass

