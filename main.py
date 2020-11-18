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


class Screen1(Screen):
    pass


class NoteApp(App):
    def build(self):
        self.transition = SlideTransition(duration=.35)
        root = ScreenManager(transition=self.transition)

        screen = Screen1(name='Screen1')
        root.add_widget(screen)
        return root


if __name__ == '__main__':
    NoteApp().run()
