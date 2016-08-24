import msg

from service import services


class Chat:
    def __init__(self, root_user):
        self.root_user = root_user
        self.login = root_user.username
        self.active_chat = None

    def p_new(self, login, _):
        try:
            services.chat.new([self.login, login])
            return msg.ok()
        except:
            return msg.fail()

    def p_chats(self, _):
        chats = services.chat.chatlist(self.login)
        if chats == None:
            return msg.fail()
        return msg.preaty(chats)

    def p_send(self, login, message, _):
        services.chat.send(self.login, login, message)
        return msg.ok()

    def p_unread(self, _):
        messages = services.chat.unread(self.login)
        return msg.preaty(messages)

    def is_allowed_to_connect(self, permission):
        return True



class ChatService:
    def p_load(self, chat_id):
        chat = services.drive.shared.readj('chat/chats/{}'.format(chat_id))
        return chat

    def p_new(self, logins):
        chat_id = '@'.join(sorted(logins))
        chat = {'logins': logins, 'messages': []}
        services.drive.shared.writej('chat/chats/{}'.format(chat_id), chat)
        logins_str = '@'.join(sorted(logins))
        for login in logins:
            services.account.get(login).drive.appendj('appdata/chat/chats', key=logins_str, value=chat_id)

    def p_send(self, login, logins, message):
        chat_id = '@'.join(sorted([login]+logins.split('@')))
        chat = services.chat.load(chat_id)
        chat['messages'].append({'login':login, 'read': [], 'message':message})
        services.chat.save(chat_id, chat)

    def p_save(self, chat_id, chat):
        services.drive.shared.writej('chat/chats/{}'.format(chat_id), chat)

    def p_unread(self, username):
        chatlist = services.account.get(username).drive.readj('appdata/chat/chats')
        result = []
        for _, chat_id in chatlist.items():
            chat = services.chat.load(chat_id)
            msgs = chat['messages']
            for ms in msgs:
                if ms['login'] != username and username not in ms['read']:
                    del ms['read']
                    result.append(ms)
        return result


        return chat.messages

