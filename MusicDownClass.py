from kivymd.uix.screen import Screen
from kivy.core.window import Window
from moviepy.editor import *
from pytube import YouTube


class MusicDownScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        Window.bind(on_request_close=self.on_window_closing)


    def startDownload():
        try:
            ytLink = link.get()
            ytObject = YouTube(ytLink, on_progress_callback=on_progress)
            video = ytObject.streams.get_highest_resolution()

            title.configure(text=ytObject.title, text_color="white")
            finishLabel.configure(text="")
            video.download(output_path="Downloads", filename=f"{video.title}.mp4")
            convert_to_mp3(video.title)
            finishLabel.configure(text="Downloaded!")
        except:
            finishLabel.configure(text="Download Error", text_color="red")

        def on_progress(stream, chunk, bytes_remaining):
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining
            percentage_of_completion = bytes_downloaded / total_size * 100
            per = str(int(percentage_of_completion))
            pPercentage.configure(text=per + "%")
            pPercentage.update()

            # Update progress bar
            progressBar.set(float(percentage_of_completion / 100))

        def convert_to_mp3(video):
            mp4_file = f"Downloads/{video}.mp4"
            mp3_file = f"Downloads/{video}.mp3"

            print(mp4_file)
            videoClip = VideoFileClip(filename=mp4_file)
            audioClip = videoClip.audio
            audioClip.write_audiofile(mp3_file)

            audioClip.close()
            videoClip.close()
            os.remove(f"Downloads/{video}.mp4")