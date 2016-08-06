class Mathe:
    def __init__(self):
        self.clients = {}
        self.a = 0

    def stop(self):
        pass

    def disconnect(self, *args):
        pass

    def connect(self, uid):
        self.clients[uid] = []

    def is_allowed_to_connect(self, permission):
        return True


class MatheService:
    def __init__(self):
        pass

    def protected_sum(self, lst, uid):
        return sum(lst)

    def protected_join(self, lst, st, uid):
        return st.join([str(l) for l in lst])

