from functools import partial


def get_service(service_name):
    pass

class ServiceInterface:
    def __init__(self, uid, service):
        self.service = service
        self.uid = uid

    def __getattr__(self, attr_name):
        attr_name = 'protected_' + attr_name
        if hasattr(self.service(attr_name)):
            return partial(getattr(self.service, attr_name), self.uid)

