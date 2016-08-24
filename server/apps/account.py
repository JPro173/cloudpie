import msg
import uuid
from service import services


class Account:
    def __init__(self, root_user):
        self.root_user = root_user

accounts = {}

class AccountInstance:
    def __init__(self, login):
        self.drive = services.drive.bake('/{}/'.format(login))
        self.login = login

    def invite(self, invitation):
        self.drive.appendj('sys/invitations', invitation)

    def notify(self, notification):
        self.drive.appendj('sys/notifications', notification)

class AccountService:
    def __init__(self):
        global accounts
        accs = [AccountInstance(dirname) for dirname in
                services.drive.root.list_dir('./users')]
        accounts = {acc.login: acc for acc in accs}

    def p_add(self, user):
        accounts[user.login] = user

    def p_get(self, username):
        return accounts.get(username)

