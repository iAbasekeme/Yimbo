from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

ArtistSubscriber = Table('artist_subscriber', Base.metadata,
                         Column('artist_id', Integer, ForeignKey(
                             'artists.id'), primary_key=True),
                         Column('user_id', Integer, ForeignKey(
                             'users.id'), primary_key=True)
                         )
