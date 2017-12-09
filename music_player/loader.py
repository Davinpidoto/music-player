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
            print(artist_name)
            session = self.dao.get_session()
            artist = self.dao.get_artist_by_name(artist_name, session)
            if artist is None:
                artist = self.dao.save_entity(Artist(name=artist_name), session)
            self.save_albums(artist, session)
            session.close()

    def save_albums(self, artist, session):
        albums = self.get_directories("%s/%s" % (Config.SOURCE_ROOT, artist.name))
        for album_name in albums:
            print("- " + album_name)
            album = self.dao.get_album_by_name(album_name, session)
            if album is None:
                album = self.dao.save_entity(Album(title=album_name, artist_id=artist.id), session)
            self.save_songs(album, artist.name, session)

    def save_songs(self, album, artist_name, session):
        songs = self.get_files("%s/%s/%s" % (Config.SOURCE_ROOT, artist_name, album.title))
        for song_file in songs:
            song = self.dao.get_song_by_file_name(song_file, session)
            if song is None:
                file = song_file[3:-4]
                self.dao.save_entity(Song(title=file, file=song_file, album_id=album.id), session)

    @staticmethod
    def get_directories(directory):
        return next(os.walk(directory))[1]

    @staticmethod
    def get_files(directory):
        return [f for f in listdir(directory) if isfile(join(directory, f)) & f.__contains__(".wav") & (f[:2] != "._")]
