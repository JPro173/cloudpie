import shlex
import uuid
from app_mng import AppManager


class Client:
    def __init__(self, conn, addr):
        self.__conn = conn
        self.addr = addr
        self.uid = str(uuid.uuid4())
        self.app_mng = AppManager(self.uid)

    def send(self, msg):
        self.__conn.send(str(msg))

    def recv(self):
        return self.__conn.recv(1024)

    def process_data(self, data):
        data = shlex.split(data)

        pid = int(data[0])
        command = data[1]
        args = data[2:]

        result = self.app_mng.call(pid, command, args)
        self.send(result)

    def loop(self):
        while True:
            data = self.recv()

            if data == b'':
                print("client {} disconnecte".format(self.addr))
                return

            self.process_data(data)
