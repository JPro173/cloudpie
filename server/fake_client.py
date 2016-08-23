import msg
import json
import uuid


from apps import system
from client import Client
from service import services
from notification import NotificationManager


class FakeClient(Client):
    def __init__(self, scen):
        self.username = ''
        self.scen = scen
        self.result = None
        self.uid = str(uuid.uuid4())
        self.apps = {0: system.System()}
        self.app_counter = 0
        self.orders = {}
        self.logged_in = False
        self.notifications = NotificationManager()
        self.scenf = getattr(self, 'scen_{}'.format(self.scen))
        services.users.add(self)

    def send(self, data):
        self.result = data

    def go(self, string):
        self.process_data(bytes(string, 'utf-8'))

    def test(self, message1, message2=None):
        if message2 is None:
            message2 = self.result
        if message2 != message1:
            raise AssertionError(
                "{}: Strings don't equals:\n{}\n{}".format(
                    self.scen,
                    message2,
                    message1
                )
            )

    def step(self, i):
        self.scenf(i)


    def scen_user00(self, step):
        if step == 0:
            #test can not do anything without register
            self.go('0 start hello')
            self.test(msg.error('You need to log in'))
        elif step == 1:
            #test success login
            self.go('0 login {} {}'.format(
                'user00',
                'qqq'
            ))
            self.test(msg.ok())
        elif step == 2:
            #test success app start
            self.go('0 start hello')
            self.test(msg.message('Program started with pid', 1))
            self.test(type(self.apps[0]).__name__, 'System')
            self.test(type(self.apps[1]).__name__, 'Hello')
        elif step == 3:
            #test hello app
            self.go('1 go 3')
            self.test(msg.message('3'))
            self.go('1 go -4')
            self.go('1 history')
            self.test(msg.message('3 -4'))
        elif step == 4:
            self.go('0 invite user01 1 1')
            self.test(msg.ok())
        elif step == 10:
            self.go('1 go 10')
            self.test(msg.message('9'))


    def scen_user01(self, step):
        if step == 0:
            #test success login
            self.go('0 login {} {}'.format(
                'user01',
                'qqq'
            ))
            self.test(msg.ok())
        elif step == 5:
            self.go('0 notifications')
            invitation_id = json.loads(self.result)[0]['uid']
            self.go('0 connect {}'.format(invitation_id))
            self.test(msg.message('Program started with pid', 1))



    def scen_cant_login(self, step):
        pass

