import json
import socket

sock = socket.socket()
sock.connect(('localhost', 5002))
sock.send(b'')
sock.recv(1024)
sock.recv(1024)
sock.recv(1024)
while True:
    sock.send(bytes(input('>> '), 'utf-8'))
    msg = str(sock.recv(1024), 'utf-8')
    try:
        data = json.loads(msg)
        status = data['status']
        message = data.get('message', status)
        status = '+' if status == 'ok' else '-'
    except:
        status = '-'
        message = 'can\'t parse ' + msg
    print("{}: {}".format(status, message))
