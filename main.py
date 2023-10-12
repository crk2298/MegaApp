import kivy
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import Screen
from kivy.core.window import Window
from kivy.config import Config

from MusicClass import MusicScreen
from WorkoutClass import WorkoutScreen
from MusicDownClass import MusicDownScreen

Window.size = (400,550)
Config.set('graphics', 'resizable', False)


class MainScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(MainScreen(name="main"))
sm.add_widget(MusicScreen(name="music"))
sm.add_widget(WorkoutScreen(name="workout"))
sm.add_widget(MusicDownScreen(name="music_down"))


class MusicApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        temp = Builder.load_file("musicgui.kv")
        return temp


if __name__ == "__main__":
    MusicApp().run()
