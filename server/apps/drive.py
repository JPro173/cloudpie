import os.path
import hmac
import hashlib


class UserDoesNotExistException(Exception):
    pass

class PathError(Exception):
    pass

class DriveError(Exception):
    pass


def prepare_path(user, sys, path, check_exists=True):
    path = os.path.join('./drive/{}/'.format(user), 'fs'*(not sys), path)
    if check_exists and not os.path.exists(path):
        raise PathError(path)
    return path

class DriveService:
    def read(self, username, path, bytes_=False):
        return open(prepare_path(username, False, path), 'r'+'b'*bytes_).read()

    def read_sys(self, username, path, bytes_=False):
        return open(prepare_path(username, True, path), 'r'+'b'*bytes_).read()

    def write(self, path, username, data, bytes_=False):
        return open(prepare_path(username, False, path), 'w'+'b'*bytes_).write(data)

    def write_sys(self, username, path, data, bytes_=False):
        return open(prepare_path(username, True, path), 'w'+'b'*bytes_).write(data)

    def checkcreds(self, login, password):
        real_hash_password = self.readline(login, './passwd').encode('hex')
        hash_password = hashlib.md5(password).hexdigest()
        hmac.compare_digest(hash_password, real_hash_password)

    def readline(self, username, path, line=0):
        try:
            return self.read(username, path).split('\n')[line]
        except IndexError:
            raise DriveError('No line in file {} with number {}'.format(path, line))
