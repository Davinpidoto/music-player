import os
from os import listdir
from os.path import isfile, join
from music_player.mysql_dao import MysqlDao, Artist, Album, Song
from music_player.config import Config


class Loader:

    def __init__(self):
        self.dao = MysqlDao()

    def sync(self):
        artists = Loader.get_directories(Config.SOURCE_ROOT)
        for artist_name in artists:
            artist = self.dao.get_artist_by_name(artist_name)
            if artist is None:
                artist = self.dao.save_entity(Artist(name=artist_name))
            self.save_albums(artist)

    def save_albums(self, artist):
        albums = self.get_directories("%s/%s" % (Config.SOURCE_ROOT, artist.name))
        for album_name in albums:
            album = self.dao.get_album_by_name(album_name)
            if album is None:
                album = self.dao.save_entity(Album(title=album_name, artist_id=artist.id))
            self.save_songs(album, artist.name)

    def save_songs(self, album, artist_name):
        songs = self.get_files("%s/%s/%s" % (Config.SOURCE_ROOT, artist_name, album.title))
        for song_file in songs:
            song = self.dao.get_song_by_file_name(song_file)
            if song is None:
                self.dao.save_entity(Song(title=song_file[3:-4], file=song_file, album_id=album.id))

    @staticmethod
    def get_directories(directory):
        return next(os.walk(directory))[1]

    @staticmethod
    def get_files(directory):
        return [f for f in listdir(directory) if isfile(join(directory, f)) & f.__contains__(".wav")]
