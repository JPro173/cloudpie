import service

def get_service(service_name):
    return ServiceInterface()

class ServiceInterface:
    def __init__(self, service_name):
        self.service = service.cervices[service_name]

    def __getattr__(self, attr_name):
        attr_name = 'protected_' + attr_name
        if hasattr(self.service(attr_name)):
            return getattr(self.service, attr_name)


class BaseApp:
    pass
