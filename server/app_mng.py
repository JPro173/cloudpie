import apps.system

from server import server


class AppManager:
    def  __init__(self):
        self.apps = {1: apps.system.System()}
        self.app_counter = 1

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
            return func(*args)
        except TypeError:
            return 'invalid arguments number'

    def sys_call(self, command, args):
        if command == 'start':
            app_name = args[0]
            try:
                app = __import__('apps.'+app_name, fromlist=('apps',))
                self.app_counter += 1
                self.apps[self.app_counter] = getattr(app, app_name.capitalize())()
                return self.app_counter
            except (ImportError, AttributeError):
                return 'bad app_name: {}'.format(app_name)
        elif command == 'stop':
            try:
                pid = int(args[0])
                if pid == 1:
                    return "you can't stop the system"
                app = self.apps[pid]
                app.stop()
                del self.apps[pid]
            except KeyError:
                return 'this app is not running!'
        elif command == 'connect':
            args = [int(arg) for arg in args]

            friend_uid, pid, permission = args

            friend = server.clients.get(friend_uid, None)
            if friend is None:
                return

            app = friend.app_mng.apps.get(pid, None)
            if app is None:
                return

            print(app)

            allowed = app.is_allowed_to_connect(permission)
            if not allowed:
                return

            self.app_counter += 1
            self.apps[self.app_counter] = app
            print('connected')

