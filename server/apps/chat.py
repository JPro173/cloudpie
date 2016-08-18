import msg
import uuid
import json

from service import services
from collections import namedtuple


class Chat:
    def __init__(self, root_uid):
        self.root_uid = root_uid
        self.a = 0
        self.login = services.users.get(root_uid).username
        self.active_chat = None
        services.chat.init(self.login)

    def stop(self):
        pass

    def disconnect(self, *args):
        pass

    def connect(self, uid):
        pass

    def p_pchat(self, login, _):
        try:
            user = services.users.get(self.root_uid)
            chat = services.chat.create([user.username, login])
            self.chat = chat
            return msg.ok()
        except:
            return msg.fail()

    def p_chats(self, _):
        chats = services.chat.chatlist(self.login)
        if chats == None:
            return msg.fail()
        return msg.preaty(chats)

    def p_choose_chat(self, chat_id, _):
        chat = services.chat.load_chat(self.login, chat_id)
        if chat == None:
            return msg.fail()
        self.chat = chat
        return msg.ok()

    def p_msg(self, message, _):
        self.active_chat.send(self.login, message)
        return msg.ok()

    def p_unread(self, _):
        return msg.preaty(self.active_chat.get_unread(self.login))

    def is_allowed_to_connect(self, permission):
        return True



class ChatService:
    def p_load_chat(self, login ,chat_id):
        admin_login, chat_name = chat_id.split('|')
        chat_data = services.drive.read(admin_login, '/appdata/chat/chats/{}'.format(chat_id))
        chat = ChatInst.from_json(chat_data)
        if not login in chat.users:
            return
        return chat

    def p_create(self, logins):
        admin_login = logins[0]
        chat_name = str(uuid.uuid4())
        chat = ChatInst(logins)
        json_data = chat.json()
        services.drive.write(admin_login, '/appdata/chat/chats/{}'.format(chat_name), data=json_data)
        chat_id = '{}|{}'.format(admin_login, chat_name)
        services.drive.append(admin_login, '/appdata/chat/chatlist', chat_id+'\n')
        return chat

    def p_chatlist(self, login):
        return services.drive.read(login, '/appdata/chat/chatlist').split('\n')

    def p_init(self, login):
        if not services.drive.exists(login, '/appdata/chat/'):
            services.drive.mkdir(login, '/appdata/chat/chats/')
            services.drive.write(login, '/appdata/chat/chatlist', '')



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

class Client:
    def __init__(self, uid):
        self.uid = uid
        self.active_chat = None

    def send(self, msg):
        if self.active_chat == None:
            return False


        return True
