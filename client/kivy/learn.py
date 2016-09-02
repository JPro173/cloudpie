import kivy
kivy.require('1.0.5')

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty


class Controller(FloatLayout):
    '''Create a controller that receives a custom widget from the kv lang file.

    Add an action to be called from the kv lang file.
    '''
    text2 = 'fuck'
    label_wid = ObjectProperty()
    info = StringProperty()

    def do_action(self):
        self.label_wid.text = self.text2#'My label after button press'
        self.info = 'New info text'

    def prr(self, data):
        print(data)
        return '12'


class LearnApp(App):

    def build(self):
        return Controller(info='Hello world')

if __name__ == '__main__':
    LearnApp().run()
