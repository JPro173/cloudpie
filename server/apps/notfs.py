import msg
from service import services

class Notfs:
    def __init__(self, root_user):
        pass

    def p_send(self, user_id, notification_text, user):
        services.users.get(user_id).notify(conn={"uid": user.uid, "text": notification_text})
        return msg.ok()
