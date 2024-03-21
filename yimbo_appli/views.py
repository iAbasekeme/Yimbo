from flask import Blueprint, jsonify
from flask import render_template
from .routes import db
from models.music import Music
from models.albums import Album
from models.artists import Artists

yb = Blueprint('views', __name__)

yb.route('/track/<int:track_id>', methods=['GET'], strict_slashes=False)


def get_track(track_id):
    '''Get the track by id'''
    track = Music.query.get(track_id)
    if track:
        return jsonify(track.serialize())
    else:
        return jsonify({'message': 'Track not found'}), 404


yb.route('/album/<int:album_id>', methods=['GET'], strict_slashes=False)


def get_album(album_id):
    '''Get album'''
    album = Album.query.get(album_id)
    if album:
        return jsonify(album.serialize()), 200
    else:
        return jsonify({'message': 'Album not found'}), 404


yb.route('/albums', methods=['GET'], strict_slashes=False)


def all_albums():
    '''A method that gets all albums'''
    albums = Album.query.all()
    if albums:
        serialize_album = [album.serialize() for album in albums]
        return jsonify(serialize_album), 200
    else:
        return jsonify({'message': 'Albums not found'}), 404


yb.route('/artist<int:artist_id>', methods=['GET'], strict_slashes=False)


def get_artist(artist_id):
    '''Get an artist'''
    artist = Artists.query.get(artist_id)
    if artist:
        return jsonify(artist.serialize())
    else:
        return jsonify({'message': 'Artist not found'}), 404
