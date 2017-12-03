import queue
import threading
import sys
from music_player.mysql_dao import MysqlDao
from music_player.osx_player import OsxPlayer
from music_player.linux_player import LinuxPlayer


class Service:

    def __init__(self):
        if sys.platform == "darwin":
            self.player = OsxPlayer()
        else:
            self.player = LinuxPlayer()
        self.dao = MysqlDao()
        self.playlist_thread = ""
        self.song_queue = queue.Queue()

    def get_artists(self):
        return self.dao.get_artists()

    def get_artist(self, artist_id):
        return self.dao.get_artist(artist_id)

    def stop(self):
        if self.playlist_thread.is_alive():
            self.song_queue.__init__()
            self.player.stop()
            self.playlist_thread.join()
        self.player.stop()

    def play_song(self, song_id):
        self.player.stop()
        song = self.dao.get_song(song_id)
        self.player.play_song(song)
        return 'Playing'

    def play_play_list(self):
        if self.song_queue == "" or self.song_queue.empty():
            return
        self.player.play_song_blocking(self.song_queue.get())
        return self.play_play_list()

    def play_album(self, album_id):
        album_to_play = self.dao.get_album(album_id)

        for song in album_to_play.songs:
            s = self.dao.get_song(str(song.id))
            self.song_queue.put(s)

        self.player.stop()
        self.playlist_thread = threading.Thread(target=self.play_play_list, args=[])
        self.playlist_thread.start()

        return "Playing"
