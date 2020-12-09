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
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.config import Config

import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

# We don't want to use fixed value for screen size.
# Config.set('graphics', 'width', '450')
# Config.set('graphics', 'height', '800')

BACKUPPATH = '/mobile-app'
LOCALPATH = 'tmp'
NUM_OF_IMAGE = 4
TOKEN = 'sl.AnB70GxfiRl-W0enzAbcvmUW4NNpIa8ophPPncZhjdqoU77bThAO6drUCEE8TOXR97Hf1zH_KMi1MXhxBKPb3Ye5Pjbd8JLRcuGpwfTqUOYjVG0EZqOSC75Wok-pObaNlIZL6kM'


class Screen1(Screen):
    def __init__(self, *args, **kwargs):
        super(Screen1, self).__init__(*args, **kwargs)
        self.callback()

    def callback(self):
        def update_height(img, *args):
            img.height = img.width

        for i in range(1, NUM_OF_IMAGE + 1):
            image = AsyncImage(source=LOCALPATH + '/' + str(i) + '.jpeg',
                               size_hint=(1, None),
                               keep_ratio=False,
                               allow_stretch=True)

            # Whenever the value of width or image_ratio changes, call the update_height funciton.
            image.bind(width=update_height, image_ratio=update_height)
            self.ids.wall.add_widget(image)


class NoteApp(App):
    def build(self):
        self.transition = SlideTransition(duration=.35)
        root = ScreenManager(transition=self.transition)

        screen = Screen1(name='Screen1')
        root.add_widget(screen)
        return root


def dropbox_login():
    # Check for an access token
    if (len(TOKEN) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token. "
                 "Open up backup-and-restore-example.py in a text editor and "
                 "paste in your token in line 14.")

    # Create an instance of a Dropbox class, which can make requests to the API.
    print("Creating a Dropbox object...")
    with dropbox.Dropbox(TOKEN) as dbx:

        # Check that the access token is valid
        try:
            dbx.users_get_current_account()
        except AuthError:
            sys.exit("ERROR: Invalid access token; try re-generating an "
                     "access token from the app console on the web.")

    return dbx


def dropbox_download_images(dbx, num_of_images):
    for i in range(1, num_of_images + 1):
        LOCALFILE = LOCALPATH + "/" + str(i) + ".jpeg"
        BACKUPFILE = BACKUPPATH + "/" + str(i) + ".jpeg"
        print("Downloading current " + BACKUPFILE +
              " from Dropbox, overwriting " + LOCALFILE + "...")
        dbx.files_download_to_file(LOCALFILE, BACKUPFILE, None)


if __name__ == '__main__':
    dbx = dropbox_login()
    dropbox_download_images(dbx, NUM_OF_IMAGE)

    NoteApp().run()
