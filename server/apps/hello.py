import msg
from collections import defaultdict
from service import services

class Hello:
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

    def public_go(self, n, uid):
        try:
            self.clients[uid].append(int(n))
            self.a += int(n)
            return msg.message(self.a)
        except:
            return msg.cast_error(0, int)

    def public_history(self, uid):
        return msg.message(services.mathe.join(self.clients[uid], ' '))

    def is_allowed_to_connect(self, permission):
        return True

class HelloService:
    pass

