import msg
from service import services


class Notes:
    def __init__(self, root_user):
        self.root_user = root_user

    def p_add(self, text, tag='', user=None):
        account = services.account.get(self.root_user.username)
        notes = account.drive.readj('/appdata/notes/notes')
        max_id = -1
        for note in notes:
            if note['id'] > max_id:
                max_id = note['id']
        account.drive.appendj(
            '/appdata/notes/notes',
            {
                'tag': tag,
                'text': text,
                'id': max_id+1
            }
        )
        return msg.ok()

    def p_notes(self, tag='', user=None):
        account = services.account.get(self.root_user.username)
        notes = account.drive.readj('/appdata/notes/notes')
        result = []
        for note in notes:
            if tag == '' or note['tag'] == tag:
                result.append(note)
        return msg.preaty(result)

    def p_delete(self, nid, user):
        account = services.account.get(self.root_user.username)
        notes = account.drive.readj('/appdata/notes/notes')
        notes = [note for note in notes if note['id'] != int(nid)]
        account.drive.writej('/appdata/notes/notes', notes)
        return msg.ok()

    def p_edit(self, nid, message, user):
        account = services.account.get(self.root_user.username)
        notes = account.drive.readj('/appdata/notes/notes')
        for i, note in enumerate(notes):
            if note['id'] == int(nid):
                note['text'] = message
                break
        else:
            return msg.fail()
        account.drive.writej('/appdata/notes/notes', notes)
        return msg.ok()

    def is_allowed_to_connect(self, perm):
        return True


