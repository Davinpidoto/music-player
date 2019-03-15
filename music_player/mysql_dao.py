from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from music_player.json_encoder import JsonSerializableBase
from music_player.config import Config

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

    db = create_engine(Config.MYSQL_URL, echo=False, pool_pre_ping=True)
    Session = sessionmaker(bind=db)
    session = Session()

    @staticmethod
    def get_artists():
        artists = MysqlDao.session.query(Artist).order_by(Artist.name).enable_eagerloads(False).all()
        MysqlDao.session.close()
        return artists

    @staticmethod
    def get_artist(artist_id):
        artist = MysqlDao.session.query(Artist).enable_eagerloads(True).get(artist_id)
        MysqlDao.session.close()
        return artist

    @staticmethod
    def get_artist_by_name(artist_name):
        return MysqlDao.session.query(Artist).enable_eagerloads(False).filter_by(name=artist_name).first()

    @staticmethod
    def get_album(album_id):
        album = MysqlDao.session.query(Album).enable_eagerloads(True).get(album_id)
        MysqlDao.session.close()
        return album

    @staticmethod
    def get_album_by_name(album_name):
        return MysqlDao.session.query(Album).enable_eagerloads(False).filter_by(title=album_name).first()

    @staticmethod
    def get_song_by_file_name(file_name):
        return MysqlDao.session.query(Song).enable_eagerloads(False).filter_by(file=file_name).first()

    @staticmethod
    def save_entity(entity):
        MysqlDao.session.add(entity)
        MysqlDao.session.commit()
        MysqlDao.session.refresh(entity)
        return entity

    @staticmethod
    def bulk_save(entities):
        MysqlDao.session.bulk_save_objects(entities)
        MysqlDao.session.commit()

    @staticmethod
    def get_song_path(song_id):
        result = MysqlDao.session.execute("""SELECT group_concat( concat( name, "/",albums.title,"/",file )) FROM songs join albums on songs.album_id = 
        albums.id inner join artists on albums.artist_id = artists.id where songs.id = """ + song_id + ';')
        rows = []
        for row in result:
            rows.append(row[0])
        MysqlDao.session.close()

        return row[0]

