import shlex
import json
import threading

from time import sleep

from app_mng import AppManager
from server import server
from connection import Connection


class FakeClient:
    def __init__(self, uid):
        self.uid = uid
        self.app_mng = AppManager(uid)
        self.connection = Connection(self.recv)
        server.connect(self)
        threading.Thread(target=self.loop, daemon=True).start()

    def loop(self):
        while True:
            sleep(0.5)
            line = input('{}> '.format(self.uid))
            parts = shlex.split(line)
            if len(parts) < 2:
                continue
            app = parts[0]
            command = parts[1]
            args = []
            if len(parts) > 2:
                args = parts[2:]
            json_data = json.dumps({'app': app, 'command': command, 'args': args})
            self.connection.recv(json_data)

    def recv(self, app, command, args):
        result = self.app_mng.call(app, command, args)
        if result is not None:
            print(result)

    def __repr__(self):
        return '<FakeClient {}>'.format(str(id(self)))
