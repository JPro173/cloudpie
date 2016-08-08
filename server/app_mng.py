import msg
import userdata
import apps.system
from server import server


class AppManager:
    def  __init__(self, user):
        self.apps = {1: apps.system.System()}
        self.app_counter = 1
        self.user = user


    def call(self, app_pid, command, args):
        app_pid = int(app_pid)
        if app_pid == 0:
            return self.sys_call(command, args)

        if not self.user.logged_in:
            return msg.need_login_error()

        app = self.apps.get(app_pid, None)
        if app is None:
            return msg.dont_exists_error(program=app_pid)

        func = getattr(app, 'public_'+command, None)
        if func is None:
            return msg.dont_exists_error(command=command)
        try:
            args.append(self.user.uid)
            return func(*args)
        except TypeError:
            return msg.args_count_error(got=len(args)-1)


    def sys_call_login(self, args):
        login = args[0]
        password = args[1]

        if userdata.checkcreds(login, password):
            self.user.logged_in = True
            self.user.login = login
            return msg.ok()
        return msg.fail()

    def sys_call_start(self, args):
        app_name = args[0]
        try:
            app = __import__('apps.'+app_name, fromlist=('apps',))
            self.app_counter += 1
            self.apps[self.app_counter] = getattr(app, app_name.capitalize())(self.user.uid)
            return msg.message('Program started with pid', self.app_counter)
        except (ImportError, AttributeError):
            return msg.dont_exists_error(program=app_name)


    def sys_call_stop(self, args):
        try:
            pid = int(args[0])
            if pid == 1:
                return msg.error('Can\'t stop system program. Use logout.')
            app = self.apps[pid]
            app.stop()
            del self.apps[pid]
        except KeyError:
            return msg.dont_exists_error(program=pid)

    def sys_call_connect(self, args):
        args = [int(arg) for arg in args]

        friend_uid, pid, permission = args
        friend = server.clients.get(friend_uid, None)
        if friend is None:
            msg.dont_exists(friend=friend_uid)
        app = friend.app_mng.apps.get(pid, None)
        if app is None:
            msg.dont_exists_error(program=pid)
        self.app_counter += 1
        self.apps[self.app_counter] = app

    def sys_call_disconnect(self, args):
        try:
            pid = int(args[0])
            if pid == 1:
                return msg.error('Can\'t stop system program. Use logout.')
            app = self.apps[pid]
            app.disconnect()
        except KeyError:
            return msg.dont_exists_error(program=pid)

    def sys_call(self, command, args):
        if command != 'login' and not self.user.logged_in:
            return msg.need_login_error()
        return getattr(self, 'sys_call_'+command)(args)


