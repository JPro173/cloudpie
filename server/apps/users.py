import msg
import uuid
import order
from service import services


class Users:
    def __init__(self, root_user):
        self.root_user = root_user

    def p_find(self, username, _):
        try:
            result = services.users.find(username, self.root_user)
            return msg.preaty(result)
        except Exception as es:
            print(str(es))

    def p_connect(self, *args):
        try:
            services.users.connect(*args)
            return msg.ok()
        except:
            raise
            return msg.fail()

    def is_allowed_to_connect(self, permission):
        return False


users = {}

class UsersService:
    def p_add(self, user):
        users[user.uid] = user

    def p_get(self, uid):
        return users.get(uid)

    def p_connect(self, uid, pid, perm, user):
        #users.get(uid).notify(conn={"uid": self_uid, "pid": pid, "perm": perm})
        oid = str(uuid.uuid4())
        users.get(uid).orders[oid] = order.new(
            uid=user.uid,
            pid=int(pid),
            perm=perm
        )

    def p_find(self, username, user):
        result = set()
        for usr in users.values():
            if usr.username == username:
                result.add(usr.uid)

        for uid in result.copy():
            if uid == user.uid:
                result.remove(uid)

        return result
