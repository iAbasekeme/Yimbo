from . import db
from sqlalchemy import create_engine, ForeignKey, DateTime
from sqlalchemy.orm import relationship
# from models.artists import artists



class Album(db.Model):
    '''An album model'''
    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    artists_id = db.Column(db.Integer, ForeignKey(
        'artists.id'), nullable=False)
    artist = relationship('Artist', backref='albums')
    release_date = db.Column(db.DateTime, nullabel=False)
    views = db.Column(db.Integer)
    release_year = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Time)

with app.app_context():
    db.create_all()
