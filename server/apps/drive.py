import os.path
import hmac
import hashlib


class PathError(Exception):
    pass

class DriveError(Exception):
    pass


class SharedDrive:
    def __init__(self):
        pass

    def ppath(self, appname, path, check_exists=True):
        if path[0] == '/':
            path = path[1:]
        path = os.path.join('./drive/shared/{}'.format(appname), path)
        path = os.path.normpath(path)
        path = os.path.abspath(path)
        if check_exists and not os.path.exists(path):
            raise PathError(path)
        return path


class DriveService:
    def __init__(self):
        self.p_shared = SharedDrive()

    def ppath(self, username, path, check_exists=True):
        if path[0] == '/':
            path = path[1:]
        path = os.path.join('./drive/{}'.format(username), path)
        path = os.path.normpath(path)
        path = os.path.abspath(path)
        if check_exists and not os.path.exists(path):
            raise PathError(path)
        return path

    def p_read(self, username, path, bytes_=False):
        try:
            return open(self.ppath(username, path), 'r'+'b'*bytes_).read()
        except PathError:
            data = b'' if bytes_ else ''
            self.p_write(username, path, data, bytes_)
            return data

    def p_write(self, username, path, data, bytes_=False):
        return open(self.ppath(username, path, check_exists=False), 'w+'+'b'*bytes_).write(data)

    def p_append(self, username, path, data, bytes_=False):
        return open(self.ppath(username, path, check_exists=False), 'a'+'b'*bytes_).write(data)

    def p_mkdir(self, username, path):
        os.makedirs(self.ppath(username, path, check_exists=False))

    def p_exists(self, username, path):
        return os.path.exists(self.ppath(username, path, check_exists=False))

    def p_checkcreds(self, username, password):
        real_hash_password = self.p_readline(username, './passwd')
        hash_password = hashlib.md5(password.encode('utf-8')).hexdigest()
        return hmac.compare_digest(hash_password, real_hash_password)

    def p_readline(self, username, path, line=0):
        try:
            return self.p_read(username, path).split('\n')[line]
        except IndexError:
            raise DriveError('No line in file {} with number {}'.format(path, line))

