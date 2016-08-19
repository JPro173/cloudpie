import msg
import apps.system
from service import services


class AppManager:
    def  __init__(self, user):
        self.apps = {1: apps.system.System()}
        self.app_counter = 1
        self.user = user


    def call(self, app_pid, command, args):
        if not self.user.logged_in:
            return msg.need_login_error()

        app = self.apps.get(app_pid, None)
        if app is None:
            return msg.dont_exists_error(program=app_pid)

        func = getattr(app, 'p_'+command, None)
        if func is None:
            return msg.dont_exists_error(command=command)
        try:
            args.append(self.user.uid)
            return func(*args)
        except TypeError:
            raise
            return msg.args_count_error(got=len(args)-1)
