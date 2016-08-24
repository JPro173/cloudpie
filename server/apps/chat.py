import msg
import uuid
import json

from service import services


class Chat:
    def __init__(self, root_user):
        self.root_user = root_user
        self.login = root_user.username
        self.active_chat = None

    def p_new(self, login, _):
        try:
            chat_id = services.chat.new([self.login, login])
            return msg.message(chat_id)
        except:
            raise
            return msg.fail()

    def p_chats(self, _):
        chats = services.chat.chatlist(self.login)
        if chats == None:
            return msg.fail()
        return msg.preaty(chats)

    def p_send(self, login, message, _):
        services.chat.send(self.login, login, message)
        return msg.ok()

    def p_messages(self, login, _):
        chat = services.chat.load(self.login, chat_id)
        return msg.preaty(chat.messages)

    def is_allowed_to_connect(self, permission):
        return True



class ChatService:
    def p_load(self, login ,chat_id):
        chat_data = services.drive.shared.read('chat/chats/{}'.format(chat_id))
        chat = ChatInst.from_json(chat_data)
        if not login in chat.logins:
            return
        return chat

    def p_new(self, logins):
        chat_id = str(uuid.uuid4())
        chat = ChatInst(logins)
        json_data = chat.json()
        services.drive.shared.write('chat/chats/{}'.format(chat_id), data=json_data)
        return chat_id

    def p_send(self, login, chat_id, message):
        chat = services.chat.load(login, chat_id)
        chat.messages.append({'login':login, 'message':message})
        services.chat.save(chat_id, chat)

    def p_save(self, chat_id, chat):
        services.drive.shared.write('chat/chats/{}'.format(chat_id), data=chat.json())

    def p_messages(self, chat_id):
        chat = services.chat.load(self.login, chat_id)
        return chat.messages



class ChatInst:
    def __init__(self, *logins):
        self.logins = set(*logins)
        self.messages = []

    @classmethod
    def from_json(cls, json_data):
        chat = ChatInst([None])
        data = json.loads(json_data)
        for message in data['messages']:
            chat.messages.append(message)
        chat.logins = set(data['logins'])
        return chat

    def json(self):
        data = {}
        data['messages'] = []
        for message in self.messages:
            data['messages'].append(message)
        data['logins'] = list(self.logins)
        return json.dumps(data)
