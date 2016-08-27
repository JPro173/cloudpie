import os.path
import shutil
import msg
import hmac
import hashlib
import json

from service import services


class Drive:
    def __init__(self, root_user):
        self.root_user = root_user

    def p_ls(self, path='', user=None):
        path = os.path.join('fs', path)
        drive = services.account.get(self.root_user.username).drive
        return msg.preaty(drive.list_dir(path))

    def p_touch(self, path, user):
        path = os.path.join('fs', path)
        drive = services.account.get(self.root_user.username).drive
        if drive.exists(path):
            return msg.fail()
        if not drive.exists(os.path.dirname(path)):
            drive.makedirs(os.path.dirname(path))
        drive.write(path, '')
        return msg.ok()

    def p_cp(self, path1, path2, user):
        path1 = os.path.join('fs', path1)
        path2 = os.path.join('fs', path2)
        drive = services.account.get(self.root_user.username).drive
        if drive.copy(path1, path2):
            return msg.ok()

    def p_rm(self, path, user):
        path = os.path.join('fs', path)
        drive = services.account.get(self.root_user.username).drive
        drive.remove(path)
        return msg.ok()

    def p_mv(self, path1, path2, user):
        path1 = os.path.join('fs', path1)
        path2 = os.path.join('fs', path2)
        drive = services.account.get(self.root_user.username).drive
        drive.move(path1, path2)
        return msg.ok()


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

    def p_read(self, path, bytes_=0):
        try:
            return open(self.ppath(path), 'r').read()
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
            open(self.ppath(path, check_exists=False))
        )
        return data

    def p_writej(self, path, data):
        return json.dump(
            data,
            open(self.ppath(path, check_exists=False), 'w+')
        )

    def p_appendj(self, path, value, key=''):
        data_curr = self.p_readj(path)
        if isinstance(data_curr, dict):
            data_curr[key] = value
        elif isinstance(data_curr, list):
            data_curr.append(value)
        else:
            raise DriveError('Can\'t append to JSON file {}'.format(path))
        self.p_writej(path, data_curr)

    def p_clean(self, path):
        path = self.ppath(path)
        shutil.rmtree(path)
        return os.makedirs(path)

    def p_makedirs(self, path):
        return os.makedirs(self.ppath(path, check_exists=False))

    def p_remove(self, path):
        path = self.ppath(path)
        if os.path.isdir(path):
            return shutil.rmtree(path)
        else:
            return os.remove(path)

    def p_copy(self, path1, path2):
        if self.p_exists(path2):
            return False
        path1 = self.ppath(path1)
        path2 = self.ppath(path2, check_exists=False)
        #if not self.p_exists(os.path.dirname(path2)):
        #    self.p_makedirs(os.path.dirname(path2))
        if os.path.isdir(path1):
            shutil.copytree(path1, path2)
        else:
            shutil.copy(path1, path2)
        return True

    def p_move(self, path1, path2):
        shutil.move(
            self.ppath(path1),
            self.ppath(path2, check_exists=False)
        )


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
        if path[0] == '/':
            path = path[1:]
        path = os.path.join(
            self.path_prefix,
            path,
            self.path_postfix
        )
        return self.drive.ppath(path, check_exists)

    def __getattr__(self, name):
        if hasattr(self, 'p_'+name):
            return getattr(self, 'p_'+name)
        raise AttributeError()

