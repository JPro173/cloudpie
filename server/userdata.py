import os.path

def checkcreds(login, password):
    try:
        data = Data(login)
    except UserDoesNotExist:
        return False
    real_password = data.read_sys('passwd').split('\n')[0]
    return password == real_password


class UserDoesNotExist(Exception):
    pass


def prepare_path(user, sys, path):
    path = os.path.join('./drive/{}/'.format(user), 'fs'*(not sys), path)
    return path

class Data:
    def __init__(self, username):
        if not os.path.isdir('./drive/{}/'.format(username)):
            raise UserDoesNotExist()
        self.username = username

    def read(self, path, bytes_=False):
        return open(prepare_path(self.username, False, path), 'r'+'b'*bytes_).read()

    def read_sys(self, path, bytes_=False):
        return open(prepare_path(self.username, True, path), 'r'+'b'*bytes_).read()

