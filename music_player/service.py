import queue
import threading
import sys
from music_player.mysql_dao import MysqlDao
from music_player.osx_player import OsxPlayer
from music_player.linux_player import LinuxPlayer
from music_player.loader import Loader


class Service:

    def __init__(self):
        if sys.platform == "darwin":
            self.player = OsxPlayer()
        else:
            self.player = LinuxPlayer()
        self.dao = MysqlDao()
        self.song_queue = queue.Queue()
        self.loader = Loader()

    def load(self):
        self.loader.sync()
        return "Synced"

    def get_artists(self):
        return self.dao.get_artists()

    def get_artist(self, artist_id):
        return self.dao.get_artist(artist_id)

    def stop(self):
        if threading.active_count() > 1:
            self.player.stop()

    def play_song(self, song_id):
        self.clear()
        self.song_queue.put(self.dao.get_song_path(song_id))
        self.play_play_list()
        return song_id

    def play_album(self, album_id):
        self.clear()
        album_to_play = self.dao.get_album(album_id)
        for song in album_to_play.songs:
            s = self.dao.get_song_path(str(song.id))
            self.song_queue.put(s)
        self.play_play_list()
        return album_to_play.title

    def clear(self):
        self.song_queue.queue.clear()
        self.stop()

    def play_play_list(self):
        if threading.active_count() == 1:
            playlist_thread = threading.Thread(target=self.play_play_list, args=[])
            playlist_thread.start()
        else:
            while self.song_queue.qsize() > 0:
                self.player.play_song_blocking(self.song_queue.get())
