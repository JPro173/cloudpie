import socket

sock = socket.socket()
sock.connect(('localhost', 8000))
while True:
    sock.send(bytes(input(), 'utf-8'))
    print(str(sock.recv(1024), 'utf-8'))
