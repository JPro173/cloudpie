import msg
from service import services


class System:
    def p_notifications(self, args):
        return msg.preaty(list(self.user.notifications.read()))

    def p_orders(self, args):
        return msg.preaty(self.user.orders)

    def p_accept(self, args):
        oid = args[0]
        order = self.user.orders.get(oid)
        if order is None:
            return msg.dont_exists_error(order_id=oid)
        if not self.apps[order.pid].is_allowed_to_connect(order.perm):
            return msg.ok()
        uid_conn = order.uid
        uapp = services.users.get(uid_conn).app_mng
        uapp.app_counter += 1
        uapp.apps[uapp.app_counter] = self.apps[order.pid]
        self.apps[order.pid].connect(uid_conn)
        return msg.ok()

    def p_login(self, args):
        try:
            username = args[0]
            password = args[1]
            if services.drive.checkcreds(username, password):
                self.user.logged_in = True
                self.user.username = username
                return msg.ok()
        except:
            return msg.fail()
        return msg.fail()

    def p_start(self, args):
        try:
            app_name = args[0]
            app = __import__('apps.'+app_name, fromlist=('apps',))
            self.app_counter += 1
            self.apps[self.app_counter] = getattr(app, app_name.capitalize())(self.user.uid)
            return msg.message('Program started with pid', self.app_counter)
        except (ImportError, AttributeError):
            return msg.dont_exists_error(program=app_name)


    def p_stop(self, args):
        try:
            pid = int(args[0])
            if pid == 1:
                return msg.error('Can\'t stop system program. Use logout.')
            app = self.apps[pid]
            app.stop()
            del self.apps[pid]
        except KeyError:
            return msg.dont_exists_error(program=pid)

    def p_disconnect(self, args):
        try:
            pid = int(args[0])
            if pid <= 1:
                return msg.error('Can\'t stop system program. Use logout.')
            app = self.apps[pid]
            app.disconnect()
        except KeyError:
            return msg.dont_exists_error(program=pid)

    def is_allowed_to_connect(self, permission):
        return False
