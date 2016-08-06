from service import services

class Hello:
    def __init__(self):
        self.clients = {}
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
        return services['mathe'].protected_sum(self.clients[uid], uid)

    def is_allowed_to_connect(self, permission):
        return True

class HelloService:
    pass

