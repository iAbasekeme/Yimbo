from . import db


class Artists(db.Model):
    '''A artists model'''
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    about = db.Column(db.String(60), nullable=False)
    # playlists = db.relationship('Playlist', back_populates="artist")
    albums = db.relationship('albums', backref="artist", lazy=True)
    tracks = db.relationship('Tracks', backref="artist", lazy=True)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    subscribers = db.relationship(
        'User', secondary=ArtistSubscriber, back_populates='subscribed_artists')

    def __repr__(self):
        """Str representation"""
        return f"User's {self.name} {self.about}"


with app.app_context():
    db.create_all()
