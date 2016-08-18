from collections import namedtuple, UserDict


Order=namedtuple('Order', 'uid pid perm')

def new(uid, pid, perm):
    return Order(uid=uid, pid=pid, perm=perm)

class OrderManager(UserDict):
    def __str__(self):pass
