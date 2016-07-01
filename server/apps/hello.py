class Hello:
    def __init__(self):
        self.a = 0

    def stop(self):
        pass

    def go(self, luid):
        self.a += 1
        return self.a

    def is_allowed_to_connect(self, permission):
        return True

