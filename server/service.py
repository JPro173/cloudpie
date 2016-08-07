import os


services = {}

def __filter_apps(files):
    return [f for f in files if f.endswith('py') and f != 'system.py' and f[0] != '_']

def start_cervices():
    for app_name in __filter_apps(os.listdir('./apps')):
        app_name = app_name[:-3]
        app = __import__('apps.'+app_name, fromlist=('apps',))
        service = getattr(app, app_name.capitalize()+'Service')()
        services[app_name] = service

