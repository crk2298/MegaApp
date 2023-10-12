from kivymd.uix.screen import Screen
import pygame
from PIL import Image  # , ImageTk
import threading
from threading import Thread
from time import sleep
import os
import math
import random
from kivy.clock import mainthread
from kivy.core.window import Window


class MusicScreen(Screen):

    def __init__(self, **kw):

        super().__init__(**kw)
        Window.bind(on_request_close=self.on_window_closing)

        # Threading variables
        self.t1 = None
        self.close_thread = False

        self.dont_update = False
        self.closing = False

    # to be setup ui
    # cover_label

    # settings
    debug = False
    auto_play = True
    shuffle_play = True

    # music/cover directory stuff
    list_of_songs = os.listdir("music")
    list_of_covers = os.listdir("img")
    n = 0

    song_name = ""
    song_len = 0
    song_offset = 0
    is_pause = False

    pygame.mixer.init()

    # @staticmethod
    def toggle_play(self, object_id):
        if object_id.name == "Pause":
            object_id.name = "Play"
            object_id.icon = "play"
            self.pause_music()
        else:
            object_id.name = "Pause"
            object_id.icon = "pause"
            self.check_loop()


    @staticmethod
    def volume(value):
        pygame.mixer.music.set_volume(value)
        # sound = SoundLoader.load()

    @staticmethod
    def music_pos(value):
        try:
            # convert song length to percentage/fraction
            song_set_time = MusicScreen.song_len * value
            MusicScreen.song_offset = song_set_time - (pygame.mixer.music.get_pos()/1000)
            if MusicScreen.debug:
                print(f"----------------\n"
                      f"song set: {song_set_time}\n"
                      f"song len: {MusicScreen.song_len}\n"
                      f"value: {value}\n"
                      f"song offset: {MusicScreen.song_offset}\n"
                      f"----------------")
            pygame.mixer.music.set_pos(song_set_time)
        except pygame.error:
            pass

    def get_album_cover(self, song_name):
        # gives each song its cover, assigned by index not name and returns null image if more songs than covers
        try:
            # img = Image.open(f"img/{MusicScreen.list_of_covers[MusicScreen.n]}")
            # print(f"img/{MusicScreen.list_of_covers[MusicScreen.n]}")
            self.ids.cover_image.source = f"img/{MusicScreen.list_of_covers[MusicScreen.n]}"
            # MusicScreen.cover_label.image = img
        except IndexError:
            img = f"null/null.png"
            self.ids.cover_image.source = img
            # MusicScreen.cover_label.image = img

        # song name label assigner
        stripped_string = song_name[6:-4]
        if len(stripped_string) > 40:
            stripped_string = f"{stripped_string[0:40]}..."
        self.ids.song_label.text = stripped_string
        # MusicScreen.song_name_label.configure(text=stripped_string)

    @staticmethod
    def format_digital_time(time_in_sec):
        mins_time = math.floor(time_in_sec / 60)
        secs_time = str((time_in_sec % 60) / 100)[2:4]
        fixed_time = [mins_time, secs_time]
        return fixed_time

    @staticmethod
    def find_first_punc(string, to_find):
        return string.index(to_find)

    @mainthread
    def update_music_bar(self):
        self.ids.music_progress_bar.value = (
                (MusicScreen.song_offset + pygame.mixer.music.get_pos() / 1000) / MusicScreen.song_len)

    # @staticmethod
    def progress(self):
        update_time = 0.4

        # gets and then converts song time from seconds to a digital format with mins
        a = pygame.mixer.Sound(f"music/{MusicScreen.list_of_songs[MusicScreen.n]}")  # Correct Name/Index
        MusicScreen.song_len = a.get_length()  # * 1.025
        song_len_format = MusicScreen.format_digital_time(MusicScreen.song_len)

        # debug stuff
        if MusicScreen.debug:
            print(f"Index: {MusicScreen.n}")
            print(f"Song Name: {MusicScreen.list_of_songs[MusicScreen.n]}")
            print(f"Time: {MusicScreen.song_len}")
            print(f"Active Threads: {threading.active_count()}")

        while (not self.close_thread and pygame.mixer.music.get_busy() or
               not self.close_thread and MusicScreen.is_pause):
            sleep(update_time)

            # updates progress bar
            if not self.dont_update:
                self.update_music_bar()

            # sets time for the active time on song to digital format
            true_time = MusicScreen.format_digital_time(round(
                MusicScreen.song_offset + pygame.mixer.music.get_pos() / 1000, 4))

            # sets label for time
            label_text = f"{true_time[0]}:{str(true_time[1])} / {song_len_format[0]}:{song_len_format[1]}"
            self.ids.time_in_sec.text = label_text

        # what happens when exiting song loop
        if MusicScreen.auto_play and not pygame.mixer.music.get_busy() and not self.closing:
            self.skip_forward()
        self.close_thread = False
        return

    # @staticmethod
    def threading_1(self):
        self.t1 = Thread(target=self.progress, daemon=False)  # could set channel
        self.t1.start()

    @staticmethod
    def song_index_validation():
        if MusicScreen.n > len(os.listdir("music")) - 1:
            MusicScreen.n = 0
        elif MusicScreen.n < 0:
            MusicScreen.n = len(os.listdir("music")) - 1

    @staticmethod
    def pause_music():
        MusicScreen.is_pause = True
        pygame.mixer.music.pause()

    @mainthread
    def play_music(self):
        # print(threading.active_count())
        # frame_size_add("up", 20)
        if threading.active_count() > 1:
            self.close_thread = True
        self.ids.music_progress_bar.value = 0
        self.song_index_validation()
        MusicScreen.song_name = f"music/{MusicScreen.list_of_songs[MusicScreen.n]}"
        self.pygame_stuff()
        self.reset()
        self.threading_1()
        self.volume(self.ids.volume_slider.value)
        MusicScreen.get_album_cover(self, MusicScreen.song_name)

    @staticmethod
    def pygame_stuff():
        pygame.mixer.music.load(MusicScreen.song_name)
        pygame.mixer.music.play(loops=0)

    @staticmethod
    def loop_song():
        pygame.mixer.music.set_pos(0)
        MusicScreen.reset()

    # @staticmethod
    def check_loop(self):
        if not pygame.mixer.music.get_busy() and not MusicScreen.is_pause:
            MusicScreen.play_music(self)
        elif MusicScreen.is_pause:
            pygame.mixer.music.unpause()
            MusicScreen.is_pause = False
        else:
            MusicScreen.loop_song()

    def on_window_closing(self, *args):
        self.closing = True
        pygame.mixer.music.stop()
        self.close_thread = True
        return False
        # music_app.destroy()

    # @staticmethod
    def skip_forward(self):
        MusicScreen.n += 1
        self.play_music()

    '''def convert_frame_geom_to_list():
        frame_geometry = music_app.winfo_geometry()
        frame_geometry_format = frame_geometry[0:find_first_punc(frame_geometry, "+")]
        new_frame_geom = [frame_geometry_format[0:find_first_punc(frame_geometry_format, "x")],
                          frame_geometry_format[find_first_punc(frame_geometry_format, "x") + 1:]]
        return new_frame_geom'''

    '''# frame adjustment
    def frame_size_add(side="up, down, left, right", amount=0):
        # input validation
        side = side.lower()

        # convert frame numbers into usable string e.g. 100x100
        frame_geometry = convert_frame_geom_to_list()
        new_frame_geom = [side, amount]
        str_frame_geom = f"{frame_geometry[0]}x{frame_geometry[1]}"

        if side == "up" or side == "down":
            # should add current width
            print("Vertical")
        elif side == "left" or side == "right":
            # should add current height
            print("Horizontal")
        else:
            print("Error in frame change!\nThe entered direction doesnt exist.")

        # applies frame size change
        self.music_app.geometry(str_frame_geom)'''

    @staticmethod
    def reset():
        MusicScreen.song_offset = 0 - pygame.mixer.music.get_pos() / 1000

    # @staticmethod
    def skip_back(self):  # Breaks the loop (need to check inside of "play_music()" like with "skip_forward")
        MusicScreen.n -= 1
        self.play_music()

    @staticmethod
    def random_n():
        MusicScreen.n = random.randint(0, len(os.listdir("music"))-1)

    @staticmethod
    def list_songs():
        song_list = os.listdir("music")
        print(len(os.listdir("music")))
        for i in song_list:
            print(f"Song {song_list.index(i)+1} is: {i}")

    '''@staticmethod
    def app_main():
        MusicScreen.list_songs()'''
