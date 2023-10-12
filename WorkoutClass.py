from kivymd.uix.screen import Screen
from kivy.core.window import Window


class WorkoutScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        Window.bind(on_request_close=self.on_window_closing)


    def on_window_closing(self, *args):
        return False
