import os.path
import hmac
import hashlib
import json


class PathError(Exception):
    pass

class DriveError(Exception):
    pass


class DriveService:
    def __init__(self):
        self.p_shared = SharedDrive()
        self.p_root = RootDrive()

    def ppath(self, path, check_exists=True):
        if path[0] == '/':
            path = path[1:]
        path = os.path.join('./drive/users/', path)
        path = os.path.normpath(path)
        path = os.path.abspath(path)
        if check_exists and not os.path.exists(path):
            raise PathError(path)
        return path

    def p_bake(self, path_prefix='', path_postfix=''):
        return BakedDrive(self, path_prefix, path_postfix)

    def p_read(self, path, bytes_=False):
        try:
            return open(self.ppath(path), 'r'+'b'*bytes_).read()
        except PathError:
            data = b'' if bytes_ else ''
            self.p_write(path, data, bytes_)
            return data

    def p_write(self, path, data, bytes_=False):
        return open(self.ppath(path, check_exists=False), 'w+'+'b'*bytes_).write(data)

    def p_append(self, path, data, bytes_=False):
        return open(self.ppath(path, check_exists=False), 'a'+'b'*bytes_).write(data)

    def p_mkdir(self, path):
        os.makedirs(self.ppath(path, check_exists=False))

    def p_exists(self, path):
        return os.path.exists(self.ppath(path, check_exists=False))

    def p_checkcreds(self, username, password):
        real_hash_password = self.p_readline('./{}/sys/passwd'.format(username))
        hash_password = hashlib.md5(password.encode('utf-8')).hexdigest()
        return hmac.compare_digest(hash_password, real_hash_password)

    def p_list_dir(self, path):
        return os.listdir(self.ppath(path))

    def p_readline(self, path, line=0):
        try:
            return self.p_read(path).split('\n')[line]
        except IndexError:
            raise DriveError('No line {} in file {}'.format(line, path))

    def p_readj(self, path):
        data = json.load(
            open(self.ppath(path))
        )
        return data
    def p_writej(self, path, data):
        return json.dump(
            open(self.ppath(path), 'w+'),
            data
        )
    def p_appendj(self, path, data):
        data_curr = self.p_readj(path)
        if isinstance(data_curr, dict):
            data_curr[data[0]] = data[1]
        elif isinstance(data_curr, list):
            data_curr.append(data)
        else:
            raise DriveError('Can\'t append to JSON file {}'.format(path))
        self.p_writej(self, path, data_curr)
class SharedDrive(DriveService):
    def __init__(self):
        pass
    def ppath(self, path, check_exists=True):
        if path[0] == '/':
            path = path[1:]
        path = os.path.join('./drive/shared/', path)
        path = os.path.normpath(path)
        path = os.path.abspath(path)
        if check_exists and not os.path.exists(path):
            raise PathError(path)
        return path

    def __getattr__(self, name):
        return getattr(self, 'p_'+name)

class RootDrive(DriveService):
    def __init__(self):
        pass
    def ppath(self, path, check_exists=True):
        if path[0] == '/':
            path = path[1:]
        path = os.path.join('./drive/', path)
        path = os.path.normpath(path)
        path = os.path.abspath(path)
        if check_exists and not os.path.exists(path):
            raise PathError(path)
        return path

    def __getattr__(self, name):
        return getattr(self, 'p_'+name)

class BakedDrive(DriveService):
    def __init__(self, drive, path_prefix, path_postfix):
        self.drive = drive
        self.path_prefix = path_prefix
        self.path_postfix = path_postfix

    def ppath(self, path, check_exists=True):
        path = os.path.join(
            self.path_prefix,
            path,
            self.path_postfix
        )
        return self.drive.ppath(path, check_exists)

    def __getattr__(self, name):
        return getattr(self, 'p_'+name)

