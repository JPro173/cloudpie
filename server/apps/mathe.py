class Mathe:
    def __init__(self, root_uid):
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

    def p_sum(self, lst):
        return sum(lst)

    def p_join(self, lst, st):
        return st.join([str(l) for l in lst])

