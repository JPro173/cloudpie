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
        self.invite_doors = {}
        self.local_notifications = NotificationManager()
        self.scenf = getattr(self, 'scen_{}'.format(self.scen))
        services.users.add(self)

    def prepare_drive(self):
        account = services.account.get(self.username)
        drive = account.drive
        drive.writej('appdata/chat/chats', {})
        drive.writej('appdata/notes/notes', [])
        drive.writej('sys/invitations', [])
        drive.writej('sys/notifcations', [])


    def send(self, data):
        self.result = data

    def go(self, string):
        self.process_data(bytes(string, 'utf-8'))

    def test(self, message1, message2=None, js=False):
        if message2 is None:
            message2 = self.result
        if js == True:
            message1 = json.loads(message1)
            message2 = json.loads(message2)
        if message2 != message1:
            raise AssertionError(
                "{}: Strings don't equals:\n{}\n{}".format(
                    self.scen,
                    message2,
                    message1
                )
            )

    def step(self, i):
        try:
            self.scenf(i)
        except:
            print("{}: {}".format(self.scen, i))
            raise


    def scen_user00(self, step):
        if step == 0:
            #test can not do anything without register
            self.go('0 start hello')
            self.test(msg.error('You need to log in'))
        elif step == 1:
            #test success login
            self.go('0 login user00 qqq')
            self.test(msg.ok())
            self.prepare_drive()
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
        elif step == 8:
            self.go('1 go 10')
            self.test(msg.message('20'))
        elif step == 9:
            self.go('0 notifications')
            self.test(
                json.loads(json.loads(self.result)['message'])[-1]['text'],
                "Hy you there"
            )
        elif step == 10:
            self.go('0 start chat')
        elif step == 12:
            self.go('2 unread')
            self.test(msg.preaty([{'login':'user01', 'message':'test_msg1'}]))
        elif step == 13:
            self.go('2 send user01 "test_msg2"')
            self.test(msg.ok())
        elif step == 15:
            self.go('0 start notes')
            self.test(msg.message('Program started with pid', 3))
            self.go('3 add "Hello world1" "film"')
            self.test(msg.ok())
            self.go('3 add "Hello world2"')
            self.go('3 notes')
            self.test(msg.preaty([{'tag': 'film', 'id': 0, 'text': 'Hello world1'}, {'tag': '', 'id': 1, 'text': 'Hello world2'}]), js=True)
            self.go('3 notes film')
            self.test(msg.preaty([{'tag': 'film', 'id': 0, 'text': 'Hello world1'}]), js=True)
            self.go('3 delete 1')
            self.test(msg.ok())
            self.go('3 notes')
            self.test(msg.preaty([{'tag': 'film', 'id': 0, 'text': 'Hello world1'}]), js=True)
            self.go('3 edit 1 "Hello world3"')
            self.test(msg.fail())
            self.go('3 edit 0 "Hello world3"')
            self.test(msg.ok())
            self.go('3 notes')
            self.test(msg.preaty([{'tag': 'film', 'id': 0, 'text': 'Hello world3'}]), js=True)
        elif step == 16:
            self.go('0 invite user01 3 1')
            self.test(msg.ok())



    def scen_user01(self, step):
        if step == 0:
            #test success login
            self.go('0 login user01 qqq')
            self.test(msg.ok())
            self.prepare_drive()
        elif step == 5:
            self.go('0 notifications')
            message = json.loads(self.result)['message']
            invitation_id = json.loads(message)[-1]['id']
            self.go('0 connect {}'.format(invitation_id))
            self.test(type(self.apps[1]).__name__, 'Hello')
            self.test(msg.message('Program started with pid', 1))
        elif step == 6:
            self.go('1 go 3')
            self.test(msg.message('2'))
            self.go('1 go 8')
            self.test(msg.message('10'))
        elif step == 7:
            self.go('1 history')
            self.test(msg.message('3 8'))
        elif step == 8:
            self.go('0 start notfs')
            self.test(msg.message('Program started with pid', 2))
            self.go('2 send user00 "Hy you there"')
            self.test(msg.ok())
        elif step == 11:
            self.go('0 start chat')
            self.test(msg.message('Program started with pid', 3))
            self.go('3 new user00')
            self.test(msg.ok())
            self.go('3 send user00 "test_msg1"')
            self.test(msg.ok())
            self.go('3 unread')
            self.test(msg.message([]))
        elif step == 14:
            self.go('3 unread')
            self.test(msg.preaty([{'login':'user00', 'message':'test_msg2'}]))
        elif step == 17:
            self.go('0 notifications')
            message = json.loads(self.result)['message']
            invitation_id = json.loads(message)[-1]['id']
            self.go('0 connect {}'.format(invitation_id))
            self.test(type(self.apps[1]).__name__, 'Hello')
            self.test(msg.message('Program started with pid', 4))
            self.go('4 edit 0 "Hello world4"')
            self.test(msg.ok())
            self.go('4 notes')
            self.test(msg.preaty([{'tag': 'film', 'id': 0, 'text': 'Hello world4'}]), js=True)
            self.go('4 add "Hello world5" "not film"')
            self.test(msg.ok())
            self.go('4 notes')
            self.test(msg.preaty([{'tag': 'film', 'id': 0, 'text': 'Hello world4'}, {'tag': 'not film', 'id': 1, 'text': 'Hello world5'}]), js=True)
            self.go('4 delete 1')
            self.test(msg.ok())
            self.go('4 notes')
            self.test(msg.preaty([{'tag': 'film', 'id': 0, 'text': 'Hello world4'}]), js=True)




    def scen_cant_login(self, step):
        if step == 0:
            self.go('0 login user00 qq')
            self.test(msg.fail())

