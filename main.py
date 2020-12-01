'''
Notes
=====

Simple application for reading/writing notes.

'''

__version__ = '1.0'

import json
from os.path import join, exists
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ListProperty, StringProperty, \
        NumericProperty, BooleanProperty, AliasProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage


class Screen1(Screen):
    def __init__(self, *args, **kwargs):
        super(Screen1, self).__init__(*args, **kwargs)
        self.callback()

    def callback(self):
        def update_height(img, *args):
            img.height = img.width / img.image_ratio

        for i in range(10):
            image = AsyncImage(source='https://bit.ly/39qjhWR',
                               size_hint=(1, None),
                               keep_ratio=True,
                               allow_stretch=True)
            image.bind(width=update_height, image_ratio=update_height)
            self.ids.wall.add_widget(image)


class NoteApp(App):
    def build(self):
        self.transition = SlideTransition(duration=.35)
        root = ScreenManager(transition=self.transition)

        screen = Screen1(name='Screen1')
        root.add_widget(screen)
        return root


if __name__ == '__main__':
    NoteApp().run()
