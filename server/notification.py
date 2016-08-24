import json


class NotificationManager:
    def __init__(self):
        self.data = []

    def append(self, category, message):
        notification = Notification(category, message)
        self.data.append(notification)

    def read(self):
        result = set()
        for notification in self.data:
            if notification.read != True:
                notification.read = True
                result.add(notification)
        return result

    def tolist(self):
        return self.data

class Notification:
    def __init__(self, category, message):
        self.category = category
        self.message = message
        self.read = False
        self.save = False

    def __repr__(self):
        return json.dumps({"category": self.category, "notification": self.message})
