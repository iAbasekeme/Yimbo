#!/usr/bin/python3
from flask import render_template, url_for, flash, redirect, session, request
from yimbo_appli import app, db, bcrypt, mail, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from yimbo_appli.forms import RegistrationForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm, UpdateAccountForm, HandleMusic, CreatePlaylistForm
from yimbo_appli.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
# for podcast
from yimbo_appli.podcast_model.model import Category, Region, Country, Podcast
from yimbo_appli.radio_model.r_model import Radio
from yimbo_appli.podcast_model.podcast_model import get_db
from sqlalchemy import inspect
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

# podcast method 
from yimbo_appli.podcast_model.podcast_methods import PodcastMethods
from yimbo_appli.radio_model.radio_methods import RadioMethods

podcast_method = PodcastMethods()
radio_method = RadioMethods()


# database part
from sqlalchemy import create_engine,  MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from yimbo_appli.podcast_model.model import Base, Country, Region, Category, Podcast

from yimbo_appli import my_session

# music method
from yimbo_appli.music_model.music_model import Genre, Music

# playlist 
from yimbo_appli.playlist_model import Playlist, PlaylistTrack
# user method
#from yimbo_appli.user_model.user_model import User

# to create a random secret token
import secrets
# To resize image
from PIL import Image
# import json
# import requests

import json
from flask import request, jsonify
import requests
from authlib.integrations.flask_client import OAuth
from main import get_music
from dotenv import load_dotenv
import os


load_dotenv()

google_client_id = os.getenv('GOOGLE_CLIENT_ID')
google_client_secret = os.getenv('GOOGLE_CLIENT_SECRET')

appConf = {
    "OAUTH2_CLIENT_ID": google_client_id,
    "OAUTH2_CLIENT_SECRET": google_client_secret,
    "OAUTH2_META_URL": "https://accounts.google.com/.well-known/openid-configuration",
    "FLASK_SECRET": "80ab528d4604e4d073b613216f6a0822"
}


app.secret_key = appConf.get("FLASK_SECRET")
oauth = OAuth(app)

oauth.register(
    "Yimbo",
    client_id=appConf.get("OAUTH2_CLIENT_ID"),
    client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email"
    },
    server_metadata_url=f'{appConf.get("OAUTH2_META_URL")}',
)




# music route

@app.route('/add_genre', methods=['GET', 'POST'])
@login_required
def add_genre():
    """method that add a new genre in the database

    Returns:
        _type_: a html page
    """
    if request.method == 'POST':
        new_genre = Genre(name=request.form['genre'])
        my_session.add(new_genre)
        my_session.commit()
        flash("Genre added successfully")
        return redirect('/add_genre')
    return render_template('add_genre.html')

def allowed_file(filename):
    """
    method to check if the file is allowed
    arguments:
        -filename: string , name of the file
    return:  Boolean, True if the file is allowed else
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add_music', methods=['GET', 'POST'])
@login_required
def add_music():
    """method that allow the admin/user to add a new audio file
        in the database
    Returns:
        _type_: html file
    """
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files or 'picture' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        picture = request.files['picture']

        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '' or picture.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Check if the file is allowed
        if file and allowed_file(file.filename) and allowed_file(picture.filename):
            music_filename = secure_filename(file.filename)
            picture_filename = secure_filename(picture.filename)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], music_filename))
            picture.save(os.path.join(app.config['UPLOAD_FOLDER'], picture_filename))
            
            # Add song to database
            new_song = Music(title=request.form['title'], artist_name=request.form['artist'], duration=request.form['duration'], genre_id=request.form['genre_id'],music_file=music_filename, picture=picture_filename)
            my_session.add(new_song)
            my_session.commit()
            flash("File Uploaded Successfully")
            return redirect('/add_music')  # Redirect after successful upload

    return render_template('add_music.html')

@app.route('/music')
@login_required
def music():
    """
    route for the music page display all genre of music
    """
    genres = my_session.query(Genre).all()
    our_musics = my_session.query(Music).all()
    return render_template('music_page.html', genres=genres,our_musics=our_musics)

@app.route('/player/<int:id>', methods=['GET','POST'])
@login_required
def player(id):
    """
    display the music player with a specific music
    argument: id: int, id of the music in the database
    """
    music = my_session.query(Music).filter_by(id=id).first()
    musics = my_session.query(Music).all()
    return render_template('music_player.html', music=music, musics=musics)

def get_song_name(id):
    """a function that return the song name from the database

    Args:
        id (int): id of the given music

    Returns:
        _type_: dict: a dictionary of the music's information
    """
    songs = my_session.query(Music).filter_by(id=id).first()
    return songs

def get_genre(id):
    """
    method to get the genre name
    Arguments:
        id: int -- id of the genre
    Return:
        dict -- informations(name and id) of the genre
    """
    genre = my_session.query(Genre).filter_by(id=id).first()
    return genre

@app.route('/music_by_genre/<int:genre_id>')
@login_required
def get_music_by_genre(genre_id):
    """
    display list of music of the specified genre
    argument:
        -int: genre's id
    return: a html file with the list of music with the specific genre
    """
    # Query all music objects with the specified genre_id
    genre = my_session.query(Genre).filter(Genre.id==genre_id).first()
    if genre:
        musics = my_session.query(Music).filter_by(genre_id=genre_id).all()
        #return render_template('music_genre.html', genre=genre, musics=musics)
        return render_template('index_2.html', genre=genre, musics=musics)
    return "Not Found"

@app.route('/playlist', methods=['GET', 'POST'])
@login_required
def playlist():
    """route of the playlist page

    Returns: the html file with all created playlist
    """
    playlists = my_session.query(Playlist).all()

    return render_template('playlist_page.html', playlists=playlists)

@app.route('/playlist/<int:playlist_id>')
@login_required
def playlist_details(playlist_id):
    """ display the list of music in the playlist

    Args:
        playlist_id (int): the id of the playlist

    Returns:
        the html page with the list of music and play option
    """
    # Query PlaylistTrack objects by playlist_id
    musics = my_session.query(PlaylistTrack).filter_by(playlist_id=playlist_id).all()
    musics_info = []
    for music in musics:
        data = get_song_name(music.music_id)
        musics_info.append({
            'music_picture': data.picture,
            'music_file': data.music_file,
            'music_id': music.music_id,
            'music_name': data.title,
            'music_artist': data.artist_name,
            'music_genre':  get_genre(data.genre_id).name,
            'music_duration': data.duration
            })
    print(musics_info)
    return render_template('playlist_details2.html', musics=musics_info)



@app.route('/playlist/create', methods=['GET', 'POST'])
@login_required
def create_playlist():
    """
    route that allow user to create a playlist and add songs into
    """
    songs = my_session.query(Music).all()
    
    genres = []
    for song in songs:
        if song.genre_id not in [genre.id for genre in genres]:
            genres.append(get_genre(song.genre_id))
        
    return render_template('handle_playlist.html', songs=songs, genres=genres)



@app.route('/add_selected_songs', methods=['POST', 'GET'])
@login_required
def add_selected_songs():
    """method that take post request from user when trying to create playlist and
        save added song in the datbase
    Returns:
        dict: a json response with status of operation (ok or error) and
    """
    selected_songs = request.json
    
    playlist_name = selected_songs.get('name')
    songs = selected_songs.get('songs')
    
    # Save the playlist to the database
    playlist = Playlist(title=playlist_name)
    my_session.add(playlist)
    my_session.flush()  # Flush to generate the playlist_id
    
    # Create PlaylistTrack objects and assign playlist_id
    playlist_tracks = []
    for idx, song_id in enumerate(songs, start=1):
        track = PlaylistTrack(playlist_id=playlist.id, music_id=song_id, track_number=idx)
        playlist_tracks.append(track)
    
    my_session.add_all(playlist_tracks)
    my_session.commit()
    my_session.close()
    
    return jsonify({'message': 'Selected songs added successfully'})



# podcast route
@app.route("/", methods=["GET", "POST"], strict_slashes=False)
@app.route("/home", methods=["GET", "POST"], strict_slashes=False)
def home():
    """This method defins the route to handle all radio streamings"""
    radio_country= "South Africa"
    podcast_country = "Kenya"
    podcast_kenya = podcast_method.display_sixpodcast(podcast_country)
    radio_sa = radio_method.display_sixradio(radio_country)
    return render_template("landing_page.html", podcast_kenya=podcast_kenya,
                           radio_sa=radio_sa)


@app.route('/podcast', methods=["GET", "POST"])
@login_required
def podcast_test():
    podcast = my_session.query(Podcast).filter_by(country_id=1).all()
    categories = my_session.query(Category).all()
    regions = my_session.query(Region).all()
    countries = my_session.query(Country).all() 
    

    return render_template('podcast_test.html', categories=categories, regions=regions, countries=countries, podcasts=podcast)


@app.route('/podcast/categories/<int:category_id>', methods=["GET", "POST"])
@login_required
def categories(category_id):
    category = my_session.query(Category).filter_by(id=category_id).first()
    if category:
        podcasts = my_session.query(Podcast).filter_by(category_id=category_id)
        return render_template('categories.html', podcasts=podcasts, data=category)
    return  jsonify({"message": "Not found."}), 404


@app.route('/podcast/region/<int:region_id>', methods=["GET", "POST"])
@login_required
def region(region_id):
    region = my_session.query(Region).filter_by(id=region_id).first()
    if region:
        podcasts_region = my_session.query(Podcast).filter_by(region_id=region_id)
        return render_template('categories.html', podcasts=podcasts_region, data=region)
    return  jsonify({"message": "Not found."}), 404

@app.route('/podcast/country/<int:country_id>', methods=["GET", "POST"])
@login_required
def country(country_id):
    country = my_session.query(Country).filter_by(id=country_id).first()
    if country:
        podcasts = my_session.query(Podcast).filter_by(country_id=country_id)
        return render_template('categories.html', podcasts=podcasts, data=country)
    return  jsonify({"message": "Not found."}), 404

@app.route('/radio', methods=["GET", "POST"])
@login_required
def radio_test():
    regions = my_session.query(Region).all()
    countries = my_session.query(Country).all()
    return render_template("radio_test.html", regions=regions, countries=countries)

@app.route('/radio/country/<int:country_id>', methods=["GET", "POST"])
@login_required
def radio_country(country_id):
    country = my_session.query(Country).filter_by(id=country_id).first()
    if country: 
        radios = my_session.query(Radio).filter_by(country_id=country_id)
        return render_template('radio.html', radios=radios, data=country)
    return  jsonify({"message": "Not found."}), 404

@app.route('/radio/region/<int:region_id>', methods=["GET", "POST"])
@login_required
def radio_region(region_id):
    region = my_session.query(Region).filter_by(id=region_id).first()
    if country:
        radios = my_session.query(Radio).filter_by(region_id=region_id)
        return render_template('radio.html', radios=radios, data=region)
    return  jsonify({"message": "Not found."}), 404


@app.route('/podcast/audio_play/<int:id>', methods=['GET', 'POST'])
@login_required
def audio_player(id):
    """
    route for the audio player page to play a specific podcast
    argument:
        -int: id of the podcast
    """
    podcast = my_session.query(Podcast).filter_by(id=id).first()
    return render_template('audio_player_test.html', podcast=podcast)



@app.route('/google-login')
def googleLogin():
    """
    method to login using google account
    """
    return  oauth.Yimbo.authorize_redirect(redirect_uri=url_for('googleCallback', _external=True))

@app.route('/sigin_google')
def googleCallback():
    """
    the callback function for the google login
    it will get the access token and user information from google
    then create an account or log in into the user account
    """
    token = oauth.Yimbo.authorize_access_token()
    session['user'] = token
    userinfo_endpoint = oauth.Yimbo.server_metadata.get('userinfo_endpoint')
    if not userinfo_endpoint:
        return 'Userinfo endpoint not found.', 400

    resp = oauth.Yimbo.get(userinfo_endpoint)
    if not resp.ok:
        return 'Failed to fetch user info from Google.', 400

    user_info = resp.json()
    email = user_info.get('email')

    # Check if the user already exists in the database
    user = User.query.filter_by(email=email).first()
    if not user:
        # If the user doesn't exist, create a new user object and add it to the database
        username = email.split('@')[0]
        user = User(email=email, username=username, password=generate_password_hash(username))
        db.session.add(user)
        db.session.commit()

    # Log the user in
    login_user(user)

    return redirect(url_for('account'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    method for registration of the user
    """
    
    if  current_user.is_authenticated:
        return  redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # let's crypt password to avoid  storing it as plain text in database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash(f'Your account has been succefully  created!, You are now able to log in ', 'sucess')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    route for the login
    """
    
    if  current_user.is_authenticated:
        return  redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        data = User.query.all()
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            #return redirect(url_for('home_page', user=user))
            return redirect(next_page) if next_page else redirect(url_for('account', user=user))
            
        else:
            flash('Login Unsuccessful. Please check your email and your password', 'danger')
    return render_template('new_login.html',form=form)


@app.route('/account')
@login_required
def account():
    """user account page with all information
    """
    return render_template('user_page.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    logout method
    """
    if current_user.is_authenticated:
        # If user is signed in with a standard account
        logout_user()
    elif 'user' in session:
        # If user is signed in with Google
        session.pop('user', None)
    return redirect(url_for('home'))


def save_picture(form_picture):
    """
    method to save the picture
    argument:
        -form_picture: file, the picture to save
    returns: string, the name of the picture saved with the path
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    #resize = (250, 250)
    #i = Image.open(form_picture)
    #i.thumbnail(resize)
    #i.save(picture_path)
    form_picture.save(picture_path)
    return picture_fn


@app.route('/account/edit', methods=['GET', 'POST'])
@login_required
def edit():
    """
    method to edit the user profile
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.password.data and form.confirm_password.data:
            if form.password.data == form.confirm_password.data:
                current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('edit'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    user = User.query.filter_by(email=current_user.email).first()
    return render_template('edit.html', user=user ,image_file=image_file, form=form)



def send_mail(user):
    """
    method to send mail
    arguments:
        -user: User, the user to send the mail
    return: None
    """
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='abdoulayesadio@gmail.com', recipients=[user.email])
    msg.body = f'''To    reset your password, visit the following link:
    {url_for('reset_password', token=token, _external=True)}
    
    Ignore this email this you are not the one who requested it
    '''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    """
    method for reset password
    """
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_mail(user)
            flash(f'''An email has been sent with instructions to reset your password.
                  Please check spam if you don't see the email''', 'info')
            return redirect(url_for('login'))
    return render_template('reset_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    method for reset password
    argument:
        -token: string, the token to reset the password
    """
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
