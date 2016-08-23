import os
from collections import UserDict


class ServiceInterface:
    def __init__(self, service):
        self.service = service

    def __getattr__(self, attr_name):
        attr_name = 'p_' + attr_name
        if hasattr(self.service, attr_name):
            return getattr(self.service, attr_name)


class Services(UserDict):
    def __getattr__(self, name):
        return self.data[name]
    def __setitem__(self, name, item):
        print(item)
        self.data[name] = ServiceInterface(item)

services = Services()

def __filter_apps(files):
    return [f for f in files if f.endswith('py') and f != 'system.py' and f[0] != '_']

def start_cervices():
    for app_name in __filter_apps(os.listdir('./apps')):
        app_name = app_name[:-3]
        app = __import__('apps.'+app_name, fromlist=('apps',))
        service_name = app_name.capitalize()+'Service'
        if hasattr(app, service_name):
            service = getattr(app, service_name)()
            services[app_name] = service

