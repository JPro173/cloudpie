import msg
from service import services


class System:
    def p_notifications(self, user):
        return msg.preaty(list(user.notifications.read()))

    def p_orders(self, user):
        return msg.preaty(user.orders)

    def p_accept(self, oid, user):
        order = user.orders.get(oid)
        if order is None:
            return msg.dont_exists_error(order_id=oid)
        if not user.apps[order.pid].is_allowed_to_connect(order.perm):
            return msg.ok()
        uid_conn = order.uid
        uapp = services.users.get(uid_conn)
        uapp.app_counter += 1
        uapp.apps[uapp.app_counter] = user.apps[order.pid]
        app = user.apps[order.pid]
        if hasattr(app, 'connect'):
                app.connect(uid_conn)
        return msg.ok()

    def p_login(self, username, password, user):
        try:
            if services.drive.checkcreds(username, password):
                user.logged_in = True
                user.username = username
                return msg.ok()
        except:
            return msg.fail()
        print('faile')
        return msg.fail()

    def p_start(self, app_name, user):
        try:
            app = __import__('apps.'+app_name, fromlist=('apps',))
            user.app_counter += 1
            user.apps[user.app_counter] = getattr(app, app_name.capitalize())(user)
            return msg.message('Program started with pid', user.app_counter)
        except (ImportError, AttributeError):
            return msg.dont_exists_error(program=app_name)


    def p_stop(self, pid, user):
        try:
            pid = int(pid)
            if pid <= 0:
                return msg.error('Can\'t stop system program. Use logout.')
            app = user.apps[pid]

            if hasattr(app, 'stop'):
                app.stop()

            del user.apps[pid]
        except KeyError:
            return msg.dont_exists_error(program=pid)

    def p_disconnect(self, pid, user):
        try:
            pid = int(pid)
            if pid <= 0:
                return msg.error('Can\'t stop system program. Use logout.')
            app = user.apps[pid]
            app.disconnect()
        except KeyError:
            return msg.dont_exists_error(program=pid)

    def is_allowed_to_connect(self, permission):
        return False
