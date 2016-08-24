import msg
from service import services

class Notfs:
    def __init__(self, root_user):
        pass

    def p_send(self, username, notification_text, user):
        services.account.get(username).notify({"uid": user.uid, "text": notification_text})
        return msg.ok()

class NotfsService:
    def p_all(self, user):
       	account = services.account.get(user.username)
        drive = account.drive
        invitations = drive.readj('sys/invitations')
        notifications = drive.readj('sys/notifications')
        local_notifications = user.local_notifications
        return invitations + notifications + local_notifications.tolist()
