from parser import get_msg_data

class Connection:
    def __init__(self, on_msg_callback):
        self.callback = on_msg_callback

    def recv(self, json_data):
        data = get_msg_data(json_data)
        app = data['app']
        command = data['command']
        args = data['args']
        self.callback(app, command, args)

