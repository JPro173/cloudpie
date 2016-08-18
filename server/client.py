import shlex
import msg
import uuid

from service import services
from app_mng import AppManager
from notification import NotificationManager


class Client:
    def __init__(self, conn, addr):
        self.__conn = conn
        self.addr = addr
        self.uid = str(uuid.uuid4())
        self.app_mng = AppManager(self)
        self.orders = {}
        self.username = ''
        self.logged_in = False
        self.notifications = NotificationManager()
        services.users.add(self)
        on_start = '''0 login user00 qqq
        0 start users
        0 start hello'''
        #2 find user00'''
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
            result = self.app_mng.call(pid, command, args)
            self.send(result)
        except:
            raise
            self.send(msg.fail())

    def loop(self):
        print("client {} connected".format(self.addr))
        while True:
            data = self.recv()

            if data == b'':
                print("client {} disconnected".format(self.addr))
                return

            self.process_data(data)
