#!/usr/bin/python3
from sqlalchemy import Column, Integer, String, ForeignKey
from podcast_model.model import Country, Region, Base
from sqlalchemy.orm import relationship

class Playlist(Base):
    """ 
    class Playlist: contains a mirror of playlist table from podcast_radio db
        args: Base inherited from the model file in the podcast_model module
    """
    __tablename__ = 'playlist'
    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    picture = Column(String(255), nullable=False, default='default.jpg')
    playlist = relationship('PlaylistTrack', backref='playlist')
    
class PlaylistTrack(Base):
    """ 
    class PlaylistTrack: contains a mirror of playlist_track table from podcast_radio db
        args: Base inherited from the model file in the podcast_model module
    """
    __tablename__ = 'playlist_track'
    id = Column(Integer, primary_key=True)
    playlist_id = Column(Integer, ForeignKey('playlist.id'))
    music_id = Column(Integer, ForeignKey('music.id'))
    track_number = Column(Integer, nullable=False)