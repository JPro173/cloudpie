import msg
import uuid
import json

from service import services
from collections import namedtuple


class Chat:
    def __init__(self, root_user):
        self.root_user = root_user
        self.a = 0
        self.login = root_user.username
        self.active_chat = None
        services.chat.init(self.login)

    def stop(self):
        pass

    def disconnect(self, *args):
        pass

    def connect(self, uid):
        pass

    def p_new(self, login, _):
        try:
            chat_id = services.chat.create([self.login, login])
            return msg.message(chat_id)
        except:
            return msg.fail()

    def p_chats(self, _):
        chats = services.chat.chatlist(self.login)
        if chats == None:
            return msg.fail()
        return msg.preaty(chats)

    def p_load(self, chat_id, _):
        chat = services.chat.load_chat(self.login, chat_id)
        if chat == None:
            return msg.fail()
        self.chat = chat
        return msg.ok()

    def p_msg(self, chat_id, message, _):
        services.chat.send(self.login, chat_id, message)
        return msg.ok()

    def p_unread(self, _):
        return msg.preaty(self.active_chat.get_unread(self.login))

    def is_allowed_to_connect(self, permission):
        return True



class ChatService:
    def p_load(self, login ,chat_id):
        admin_login, chat_name = chat_id.split('|')
        chat_data = services.drive.read(admin_login, '/appdata/chat/chats/{}'.format(chat_id))
        chat = ChatInst.from_json(chat_data)
        if not login in chat.users:
            return
        return chat

    def p_new(self, logins):
        chat_id = str(uuid.uuid4())
        chat = ChatInst(logins)
        json_data = chat.json()
        services.drive.shared.write('chat', '/appdata/chat/chats/{}'.format(chat_id), data=json_data)
        return chat

    def p_chatlist(self, login):
        return services.drive.read(login, '/appdata/chat/chatlist').split('\n')


class ChatInst:
    def __init__(self, *logins):
        self.admin_login = logins[0]
        self.logins = set(*logins)
        self.messages = []

    @classmethod
    def from_json(cls, json_data):
        chat = ChatInst([None])
        data = json.loads(json_data)
        for message in data['messages']:
            chat.messages.append(message_from_json(message))
        chat.logins = set(*data['logins'])
        chat.admin_login = data['admin_login']
        return chat

    def json(self):
        data = {}
        data['messages'] = []
        for message in self.messages:
            data['messages'].append(dict(message._asdict()))
        data['logins '] = list(self.logins)
        data['admin_login'] = self.admin_login
        return json.dumps(data)

    def get_unread(self, self_login):
        result = []
        for message in self.messages[:100]:
            if message.to == self_login and not message.read:
                result.append(message)
        return result

    def send(self, login1, login2, message):
        self.messages.append(Message(login1, login2, 0, message, False))

Message = namedtuple('Message', 'sender time msg read')

def message_from_json(json_data):
    data = json.loads(json_data)
    return Message(**data)

