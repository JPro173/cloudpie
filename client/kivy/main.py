import json
import socket

import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput


sock = socket.socket()
sock.connect(('localhost', 5002))

sock.send(b'')
sock.recv(1024)
sock.recv(1024)
sock.recv(1024)

input_field = None
summary_lbl = None
history_lbl = None

def my_event():
    try:
        value = int(input_field.text)
        sock.send(b'2 go {}'.format(value))
        data = sock.recv(1024).encode('utf-8')
        summary_lbl.text = 'Summary: '+json.loads(data)['message']
        sock.send(b'2 history')
        data = sock.recv(1024).encode('utf-8')
        history_lbl.text = 'History: '+json.loads(data)['message']
        input_field.background_color = (1, 1, 1, 1)
    except Exception as e:
        print(str(e))
        input_field.background_color = (1, 0, 0, 1)


class Form(BoxLayout):
    def __init__(self, fields):
        global input_field
        BoxLayout.__init__(self)
        self.spacing = 2
        self.size_hint = (1, None)
        self.size = (0, 50)
        self.pos_hint = {'y': 0.9}
        submit_button = Button(text='Send')
        submit_button.on_press = my_event
        submit_button.size_hint = (None, None)
        submit_button.size = (100, 50)
        input_field = TextInput(text='0')
        self.add_widget(submit_button)
        self.add_widget(input_field)


class TestApp(App):
    def build(self):
        global summary_lbl, history_lbl
        root = BoxLayout(spacing=3, orientation='vertical')
        root.add_widget(Form())
        history_lbl = Label(text='History:', halign="left", valign="top")
        history_lbl.bind(size=history_lbl.setter('text_size'))
        summary_lbl = Label(text='Summary: 0', halign="left", valign="top")
        summary_lbl.bind(size=summary_lbl.setter('text_size'))
        summary_lbl.size_hint = (1, None)
        summary_lbl.size = (0, 50)
        root.add_widget(summary_lbl)
        root.add_widget(history_lbl)
        root.add_widget(Widggg())
        return root

class Widggg(Widget):
    pass

app = TestApp()
app.run()
