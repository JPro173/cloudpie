import msg
from collections import defaultdict
from service import services

class Hello:
    def __init__(self, root_user):
        self.root_user = root_user
        self.clients = defaultdict(list)
        self.a = 0

    def stop(self):
        pass

    def disconnect(self, *args):
        pass

    def connect(self, user):
        self.clients[user.uid] = []

    def p_go(self, n, user):
        try:
            self.clients[user.uid].append(int(n))
            self.a += int(n)
            return msg.message(self.a)
        except:
            return msg.cast_error(0, int)

    def p_history(self, user):
        return msg.message(services.mathe.join(self.clients[user.uid], ' '))

    def is_allowed_to_connect(self, permission):
        return True

class HelloService:
    pass

