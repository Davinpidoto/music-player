from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from music_player.json_encoder import JsonSerializableBase
import os

Base = declarative_base(cls=(JsonSerializableBase,))


class Artist(Base):
    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    albums = relationship("Album", lazy='joined')


class Album(Base):
    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    artist_id = Column(Integer, ForeignKey('artists.id'))
    songs = relationship("Song", lazy='joined')


class Song(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    file = Column(String)
    album_id = Column(Integer, ForeignKey('albums.id'))


class MysqlDao:

    def __init__(self):
        pass

    @staticmethod
    def get_artists():
        session = MysqlDao.get_session()
        artists = session.query(Artist).enable_eagerloads(False).all()
        session.close()
        return artists

    @staticmethod
    def get_artist(artist_id):
        session = MysqlDao.get_session()
        artist = session.query(Artist).enable_eagerloads(True).get(artist_id)
        session.close()
        return artist

    @staticmethod
    def get_album(album_id):
        session = MysqlDao.get_session()
        album = session.query(Album).enable_eagerloads(True).get(album_id)
        session.close()
        return album

    @staticmethod
    def get_song_path(song_id):
        session = MysqlDao.get_session()
        result = session.execute("""SELECT group_concat( concat( name, "/",albums.title,"/",file )) FROM songs join albums on songs.album_id = 
        albums.id inner join artists on albums.artist_id = artists.id where songs.id = """ + song_id + ';')
        rows = []
        for row in result:
            rows.append(row[0])
        session.close()

        return row[0]

    @staticmethod
    def get_session():
        url = os.environ['MYSQL_URL']
        db = create_engine(url, echo=False)
        Session = sessionmaker(bind=db)
        return Session()
