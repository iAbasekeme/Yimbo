from . import db
from sqlalchemy import Interval
from sqlalchemy.orm import relationship
from datetime import date
# from models.artists import artists



class Album(db.Model):
    '''An album model'''
    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    artists_id = db.Column(db.Integer, ForeignKey(
        'artist.id'), nullable=False)
    artist = db.relationship('Artist', backref='albums')
    release_date = db.Column(db.DateTime, nullabel=False)
    views = db.Column(db.Integer)
    release_year = db.Column(db.DateTime, nullable=False)
    duration = db.Column(Interval)
    tracks = db.relationship('Music', back_populates='album')

    def calculate_duration(self):
        '''A method that calculates duration'''
        total_duration = timedelta(seconds=0)
        for track in self.tracks:
            if track.duration:
                total_duration += track.duration
        return total_duration

    def serialize(self):
        current_year = datetime.now().year
        return {
            'id': self.id,
            'title': self.title,
            'artists_id': self.artists_id,
            'release_date': self.release_date.strftime('%B %d %Y') if self.release_date else None,
            'views': self.views,
            'release_year': date.today().year,
            'duration': str(self.calculate_duration()) if self.duration else None
        }

with app.app_context():
    db.create_all()
