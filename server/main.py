from server import server

from fake_client import FakeClient


FakeClient(0)
FakeClient(1)

server.listen(5000)

