import shlex
import msg
import uuid

from apps import system
from service import services
from notification import NotificationManager


class Client:
    def __init__(self, conn, addr):
        self.__conn = conn
        self.addr = addr
        self.uid = str(uuid.uuid4())
        self.apps = {0: system.System()}
        self.app_counter = 0
        self.orders = {}
        self.username = ''
        self.invite_doors = {}
        self.logged_in = False
        self.local_notifications = NotificationManager()
        services.users.add(self)
        on_start = '''0 login user00 qqq
        0 start users
        0 start hello'''
        for line in on_start.split('\n'):
            self.process_data(bytes(line, 'utf-8'))

    def send(self, msg):
        self.__conn.send(bytes(str(msg), 'utf-8'))

    def recv(self):
        return self.__conn.recv(1024)

    def notify(self, **kwargs):
        self.notifications.append(*(list(kwargs.items())[0]))

    def process_data(self, data):
        data = shlex.split(str(data, 'utf-8'))
        try:
            pid = int(data[0])
            command = data[1]
            args = data[2:]
            result = self.call_func(pid, command, args)
            self.send(result)
        except:
            raise
            self.send(msg.fail())

    def call_func(self, pid, command, args):
        if (pid != 0 or command != 'login') and not self.logged_in:
            return msg.error('You need to log in')

        app = self.apps.get(pid, None)
        if app is None:
            return msg.dont_exists_error(program=pid)

        func = getattr(app, 'p_'+command, None)
        if func is None:
            return msg.dont_exists_error(command=command)
        try:
            return func(*args, _=None)
        except TypeError:
            pass
        try:
            return func(*args, user=self)
        except TypeError:
            raise
            return msg.args_count_error(got=len(args)-1)

    def loop(self):
        print("client {} connected".format(self.addr))
        while True:
            data = self.recv()

            if data == b'':
                print("client {} disconnected".format(self.addr))
                return

            self.process_data(data)
