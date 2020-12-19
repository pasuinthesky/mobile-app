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

import pyodbc

# We don't want to use fixed value for screen size.
# Config.set('graphics', 'width', '450')
# Config.set('graphics', 'height', '800')

BACKUPPATH = '/mobile-app'
LOCALPATH = 'tmp'
NUM_OF_IMAGE = 0
NUM_RECIPE_IN_SCREEN = 10
TOKEN = 'sl.AnrteHEUq8ZDhXhdOIzCk1HSkHJ1gCfHQtrBJKoHIRAkI_8mPik5Nv2vZOt5RT7VUzAO6oHDJgHiGc5X1iHC515DihOom3FUW9dttVnK3ma4LVpxDa1rTD-3VxTgkKS4ZQDN9gg'


class Screen1(Screen):
    def __init__(self, *args, **kwargs):
        super(Screen1, self).__init__(*args, **kwargs)
        self.callback()

    def callback(self):
        def update_height(img, *args):
            img.height = img.width

        for i in range(NUM_OF_IMAGE):
            image = AsyncImage(source=LOCALPATH + '/' + recipes[i][2],
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
    for i in range(num_of_images):
        LOCALFILE = LOCALPATH + "/" + recipes[i][2]
        BACKUPFILE = BACKUPPATH + "/" + recipes[i][2]
        print("Downloading current " + BACKUPFILE +
              " from Dropbox, overwriting " + LOCALFILE + "...")
        dbx.files_download_to_file(LOCALFILE, BACKUPFILE, None)


if __name__ == '__main__':
    server = 'tcp:mobile-app-db-srv.database.windows.net,1433'
    database = 'mobile-app-db'
    username = 'mobile-app-db-admin'
    password = '2020nov10.'
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server +
        ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = connection.cursor()

    #Sample select query
    cursor.execute("SELECT * FROM Recipe")
    recipes = cursor.fetchmany(NUM_RECIPE_IN_SCREEN)
    NUM_OF_IMAGE = len(recipes)
    for r in recipes:
        print(r[0], r[1], r[2])

    dbx = dropbox_login()
    dropbox_download_images(dbx, NUM_OF_IMAGE)

    NoteApp().run()
