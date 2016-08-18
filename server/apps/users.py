import msg
import uuid
import order
from service import services


class Users:
    def __init__(self, root_uid):
        self.root_uid = root_uid

    def p_find(self, username, _):
        try:
            result = services.users.find(username, self.root_uid)
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

    def p_connect(self, uid, pid, perm, self_uid):
        #users.get(uid).notify(conn={"uid": self_uid, "pid": pid, "perm": perm})
        oid = str(uuid.uuid4())
        users.get(uid).orders[oid] = order.new(
            uid=self_uid,
            pid=int(pid),
            perm=perm
        )

    def p_find(self, username, self_uid):
        result = set()
        for user in users.values():
            if user.username == username:
                result.add(user.uid)

        for uid in result.copy():
            if uid == self_uid:
                result.remove(uid)

        return result
