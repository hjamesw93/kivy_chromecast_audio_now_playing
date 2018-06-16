from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
import pychromecast
import time


class NowPlayingScreen(GridLayout):
    def __init__(self, cc, **kwargs):
        super(NowPlayingScreen, self).__init__(**kwargs)
        self.cols = 3
        time.sleep(1)

        self.track_artist = Label(text=cc.media_controller.status.artist)
        self.track_title = Label(text=cc.media_controller.status.title)

        image = next(i for i in cc.media_controller.status.images
                             if i.height > 500)

        self.album_art = AsyncImage(source=image.url)

        # Add the UI elements to the layout:
        self.add_widget(self.track_artist)
        self.add_widget(self.track_title)
        self.add_widget(self.album_art)

    def update_track_title(self, text):
        self.track_title.text = text

    def update_track_artist(self, text):
        self.track_artist.text = text

    def update_album_art(self, media_images):
        self.album_art.source = \
            next(i for i in media_images if i.height > 500).url
        self.album_art.reload()


class NowPlaying(App):
    def build(self):

        chromecasts = pychromecast.get_chromecasts()
        chromecast = next(cc for cc in chromecasts if
                          cc.device.friendly_name == "Living Room Speaker")

        ui = NowPlayingScreen(chromecast)

        listener_cast = StatusListener(chromecast.name, chromecast, ui)
        chromecast.register_status_listener(listener_cast)

        listener_media = StatusMediaListener(chromecast.name, chromecast, ui)
        chromecast.media_controller.register_status_listener(listener_media)

        return ui


class StatusListener:
    def __init__(self, name, cast, ui):
        self.name = name
        self.cast = cast

    def new_cast_status(self, status):
        print('[',time.ctime(),' - ', self.name,'] status chromecast change:')
        print(status)


class StatusMediaListener:
    def __init__(self, name, cast, ui):
        self.name = name
        self.cast= cast
        self.ui = ui

    def new_media_status(self, status):
        self.ui.update_track_title(status.title)
        self.ui.update_track_artist(status.artist)
        self.ui.update_album_art(status.images)


if __name__ == '__main__':
    NowPlaying().run()
