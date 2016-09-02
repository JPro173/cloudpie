import htmlPy
import socket
import json
import os


sock = socket.socket()
sock.connect(('localhost', 5002))
sock.send(b'')
sock.recv(1024)
sock.recv(1024)
sock.recv(1024)

app = htmlPy.AppGUI(title=u"Python Best Ever", maximized=True)

app.template_path = os.path.abspath("./html")
app.static_path = os.path.abspath("./html")

template_name = 'index.html'

app_data = {
    'val': '0'
}

def processor(response):
    response = str(response)
    response = json.loads(response)['message']
    print(response)
    command, data = response.split('#')
    if '@' in command:
        command, subcommand = command.split('@')
    if command == 'put':
        app_data[subcommand] = data


class App(htmlPy.Object):
    def __init__(self):
        super(App, self).__init__()

    @htmlPy.Slot(str)
    def link(self, url):
        template_name = str(url)
        app.template = (template_name, app_data)

    @htmlPy.Slot(str)
    def command(self, cmd):
        cmd = bytes(cmd)
        sock.send(cmd)
        response = sock.recv(1024)
        processor(response)
        app.template = (template_name, app_data)


app.template = (template_name, app_data)

app.bind(App())

app.start()

