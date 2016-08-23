import msg
import uuid
from service import services


class Account:
    def __init__(self, root_user):
        self.root_user = root_user

    def p_invite(self, username, pid, perm):
        services.account.get(username).invite(pid, perm)

accounts = {}

class AccountInstance:
    def __init__(self, login):
        self.drive = services.drive.bake('/{}/'.format(login))
        self.login = login

    def invite(self, username, pid, perm):
        uid = str(uuid.uuid4())
        self.drive.appendj('sys/invitations', {'uid': uid, 'username': username, 'pid': pid, 'perm': perm})
        return msg.ok()

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

