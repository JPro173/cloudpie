import apps.system
import login

from server import server


class AppManager:
    def  __init__(self, uid):
        self.apps = {1: apps.system.System()}
        self.app_counter = 1
        self.uid = uid


    def call(self, app_pid, command, args):
        app_pid = int(app_pid)
        if app_pid == 0:
            d = self.sys_call(command, args)
            return d

        app = self.apps.get(app_pid, None)
        if app is None:
            return

        func = getattr(app, command, None)
        if func is None:
            return
        try:
            args.append(self.uid)
            return func(*args)
        except TypeError:
            return 'invalid arguments number'


    def sys_call_login(self, args):
        login = args[0]
        password = args[1]

        if login.login(login, password):
            return 'ok'
        return 'fail'

    def sys_call_start(self, args):
        app_name = args[0]
        try:
            app = __import__('apps.'+app_name, fromlist=('apps',))
            self.app_counter += 1
            self.apps[self.app_counter] = getattr(app, app_name.capitalize())(self.uid)
            return self.app_counter
        except (ImportError, AttributeError):
            return 'bad app_name: {}'.format(app_name)


    def sys_call_stop(self, args):
        try:
            pid = int(args[0])
            if pid == 1:
                return "you can't stop the system"
            app = self.apps[pid]
            app.stop()
            del self.apps[pid]
        except KeyError:
            return 'this app is not running!'

    def sys_call_connect(self, args):
        args = [int(arg) for arg in args]

        friend_uid, pid, permission = args
        friend = server.clients.get(friend_uid, None)
        if friend is None:
            return
        app = friend.app_mng.apps.get(pid, None)
        if app is None:
            return
        self.app_counter += 1
        self.apps[self.app_counter] = app
        print('connected')

    def sys_call_disconnect(self, args):
        try:
            pid = int(args[0])
            if pid == 1:
                return "you can't stop the system"
            app = self.apps[pid]
            app.disconnect()
        except KeyError:
            return 'this app is not running!'

    def sys_call(self, command, args):
        return getattr(self, 'sys_call_'+command)(args)


