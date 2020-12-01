#!/usr/bin/env python
from kivy.config import Config
from kivy.uix.image import AsyncImage

Config.set('kivy', 'log_level', 'debug')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

kv = """
<Test>:
    ScrollView:
        id: scroll
        GridLayout:
            id: wall
            cols: 3
            size_hint_y:  None
            height: self.minimum_height
"""

Builder.load_string(kv)


class Test(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.callback()

    def callback(self):
        def update_height(img, *args):
            img.height = img.width / img.image_ratio

        for i in range(100):
            image = AsyncImage(source='https://goo.gl/MDPwMF',
                               size_hint=(1, None),
                               keep_ratio=True,
                               allow_stretch=True)
            image.bind(width=update_height, image_ratio=update_height)
            self.ids.wall.add_widget(image)


class TestApp(App):
    def build(self):
        return Test()


if __name__ == '__main__':
    TestApp().run()