#!/usr/bin/python3
from flask import render_template, url_for, flash, redirect, session, request
from yimbo_appli import app, db, bcrypt, mail, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from yimbo_appli.forms import RegistrationForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm, UpdateAccountForm, HandleMusic, CreatePlaylistForm
from yimbo_appli.models import User, Music, Playlist
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
# for podcast
from yimbo_appli.model import Category, Region, Country, Podcast
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
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from podcast_model.model import Base, Country, Region, Category, Podcast

# music method
from yimbo_appli.music_model.music_model import Genre, Music



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

# Connection to the database
engine = create_engine('mysql+mysqldb://root:elpastore@localhost:3306/podcast_radio_database')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


# music route

@app.route('/add_genre', methods=['GET', 'POST'])
def add_genre():
    if request.method == 'POST':
        new_genre = Genre(name=request.form['genre'])
        session.add(new_genre)
        session.commit()
        flash("Genre added successfully")
        return redirect('/add_genre')
    return render_template('add_genre.html')

def allowed_file(filename):
    """
    method to check if the file is allowed
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/add_music', methods=['GET', 'POST'])
def add_music():
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
            session.add(new_song)
            session.commit()
            flash("File Uploaded Successfully")
            return redirect('/add_music')  # Redirect after successful upload

    return render_template('add_music.html')

@app.route('/music')
def music():
    """
    route for the music page display all genre of music
    """
    genres = session.query(Genre).all()
    our_musics = session.query(Music).all()
    return render_template('music_page.html', genres=genres,our_musics=our_musics)

@app.route('/all_music')
def all_music():
    """
    display all music in the database
    """
    our_musics = session.query(Music).all()
    return render_template('music.html', our_musics=our_musics)


@app.route('/player/<int:id>', methods=['GET','POST'])
def player(id):
    """
    display the music player with a specific music
    """
    music = session.query(Music).filter_by(id=id).first()
    musics = session.query(Music).all()
    return render_template('spotify_player.html', music=music, musics=musics)


@app.route('/music_by_genre/<int:genre_id>')
def get_music_by_genre(genre_id):
    """
    display list of music of the specified genre
    """
    # Query all music objects with the specified genre_id
    genre = session.query(Genre).filter(Genre.id==genre_id).first()
    musics = session.query(Music).filter_by(genre_id=genre_id).all()
    return render_template('index_2.html', genre=genre, musics=musics)







# podcast route

@app.route("/sort_category", methods=["GET", "POST"], strict_slashes=False)
def sort_category():
    """ retrieve the category name and get all podcasts belonging
        to that group
    """ 

    # retrive the request
    group_names = request.args.get("category")
    table_names = request.args.get("table_names")
    category_info = podcast_method.get_podcastsInEachCategory(group_names)
    pic_names = podcast_method.get_imageFile_name("/home/elpastore/ALX-program/portifolio_project/Yimbo/yimbo_appli/static/pics") # use the full path of the server
    podcast_info =  podcast_method.get_linkFromFile(category_info, pic_names)
    
    # Render the template and pass the category and table names as context variables
    return render_template("new.html", group_names=group_names,
                           podcast_info=podcast_info)


@app.route("/sort_region", methods=["GET", "POST"], strict_slashes=False)
def sort_region():
    """ retrieve the region name and get all podcasts belonging
        to that group
    """
    group_names = request.args.get("region")
    table_names = request.args.get("table_names")
    category_info = podcast_method.get_podcastsInEachRegion(group_names)
    image_dir = "/home/elpastore/ALX-program/portifolio_project/Yimbo/yimbo_appli/static/pics" # use the full path of the server
    pic_names = podcast_method.get_imageFile_name(image_dir)
    podcast_info =  podcast_method.get_linkFromFile(category_info, pic_names)

    return render_template("new.html",
                           group_names=group_names,
                           podcast_info=podcast_info)


@app.route("/sort_country", methods=["GET", "POST"], strict_slashes=False)
def sort_country():
    """ retrieve the country name and get all podcasts belonging
        to that group
    """
    
    # retrive the request
    group_names = request.args.get("country")
    table_names = request.args.get("table_names")
    category_info = podcast_method.get_podcastsInEachCountry(group_names)
    image_dir = "/home/elpastore/ALX-program/portifolio_project/Yimbo/yimbo_appli/static/pics" # use the full path of the server
    pic_names = podcast_method.get_imageFile_name(image_dir)
    podcast_info =  podcast_method.get_linkFromFile(category_info, pic_names)

    # Render the template and pass the category and table names as context variables
    return render_template("new.html",
                           group_names=group_names,
                           podcast_info=podcast_info,
                           )


@app.route("/user_radio", methods=["GET", "POST"], strict_slashes=False)
def user_radio():
    """This method defins the route to handle all radio streamings"""
    table_names = podcast_method.get_table_name()
    country_names = podcast_method.country_names()
    region_names = podcast_method.region_names()
    return render_template("podcast_page.html",
                               table_names=table_names,
                               country_names=country_names,
                               region_names=region_names)


@app.route("/sort_radioByRegion", methods=["GET", "POST"], strict_slashes=False)
def sort_radioByRegion():
    """ retrieve the region name and get all podcasts belonging
        to that group
    """
    group_names = request.args.get("region")
    table_names = request.args.get("table_names")
    category_info = radio_method.get_radioInEachRegion(group_names)
    image_dir = "/home/elpastore/ALX-program/portifolio_project/Yimbo/yimbo_appli/static/r_pics" # use the full path of the server
    pic_names = podcast_method.get_imageFile_name(image_dir)
    radio_info =  podcast_method.get_linkFromFile(category_info, pic_names)

    return render_template("new.html",
                           group_names=group_names,
                           radio_info=radio_info)


@app.route("/sort_RadioByCountry", methods=["GET", "POST"], strict_slashes=False)
def sort_RadioByCountry():
    """ retrieve the country name and get all podcasts belonging
        to that group
    """
    # retrive the request
    group_names = request.args.get("country")
    table_names = request.args.get("table_names")
    category_info = radio_method.get_radioInEachCountry(group_names)
    image_dir = "/home/elpastore/ALX-program/portifolio_project/Yimbo/yimbo_appli/static/r_pics" # use the full path of the server
    pic_names = podcast_method.get_imageFile_name(image_dir)
    radio_info =  podcast_method.get_linkFromFile(category_info, pic_names)

    # Render the template and pass the category and table names as context variables
    return render_template("new.html",
                           group_names=group_names,
                           radio_info=radio_info,
                           )


@app.route("/home", methods=["GET", "POST"], strict_slashes=False)
def home():
    """This method defins the route to handle all radio streamings"""
    radio_country= "South Africa"
    podcast_country = "Kenya"
    podcast_kenya = podcast_method.display_sixpodcast(podcast_country)
    radio_sa = radio_method.display_sixradio(radio_country)
    return render_template("landing_page.html", podcast_kenya=podcast_kenya,
                           radio_sa=radio_sa)


@app.route("/podcast_audio_player", methods=["GET", "POST"], strict_slashes=False)
def podcast_audio_player():
    """handles the audio_player"""
    name = request.args.get("name")

    description = request.args.get("description")

    image = request.args.get("img")

    audio_id = request.args.get("audio_id")
    audio_dir = "/home/elpastore/ALX-program/portifolio_project/Yimbo/yimbo_appli/static/p_music"
    audio_files = podcast_method.get_audioFiles(audio_dir)
    fileName = podcast_method.get_linkFromFile(audio_id, audio_files)
    errMessage = None
    dirName = "p_music"
 
    if fileName == "Audio content is Unavailable":
        errMessage = fileName
        return render_template("errMessage.html", errMessage=errMessage)
    else:
        return render_template("audio_player.html", name=name,
                           image=str(image), dirName=dirName,
                           description=description,
                           fileName=fileName)
    
    
@app.route("/radio_audio_player", methods=["GET", "POST"], strict_slashes=False)
def radio_audio_player():
    """handles the audio_player"""
    name = request.args.get("name")
    description = request.args.get("description")
    image = request.args.get("img")
    audio_id = request.args.get("audio_id")

    audio_dir = "/home/elpastore/ALX-program/portifolio_project/Yimbo/yimbo_appli/static/r_music"
    audio_files = podcast_method.get_audioFiles(audio_dir)
    fileName = podcast_method.get_linkFromFile(audio_id, audio_files)
    dirName = "r_music"
    

    errMessage = None
 
    if fileName == "Audio content is Unavailable":
        errMessage = fileName
        return render_template("errMessage.html", errMessage=errMessage)
    else:
        return render_template("audio_player.html", name=name,
                           image=str(image), dirName=dirName,
                           fileName=fileName,
                           description=description)

@app.route("/podcast_main", methods=["GET", "POST"], strict_slashes=False)
def podcast_main():
    category_names = podcast_method.category_names()
    table_names = podcast_method.get_table_name()
    country_names = podcast_method.country_names()
    region_names = podcast_method.region_names()

    return render_template("podcast_page.html",
                           category_names=category_names,
                           table_names=table_names,
                           country_names=country_names,
                           region_names=region_names)





@app.route('/')
@app.route('/home')
def home_page():
    """
    route for the landing page define by wisdom
    """
    return  render_template('two_clone.html')
    # return render_template('main_page.html', session=session.get('user'))

@app.route('/google-login')
def googleLogin():
    """
    method to login using google account
    """
    return  oauth.Yimbo.authorize_redirect(redirect_uri=url_for('googleCallback', _external=True))

@app.route('/sigin_google')
def googleCallback():
    """
    the callback function
    
    token = oauth.Yimbo.authorize_access_token()
    session['user'] = token
    return redirect(url_for('account')) 
    #return redirect(url_for("home_page"))"""
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
    method for registration"""
    
    if  current_user.is_authenticated:
        return  redirect(url_for('home_page'))
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
    route for the login"""
    
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
    # return render_template('user.html')
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('new_user_page.html', image_file=image_file)
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
    return redirect(url_for('home_page'))


def save_picture(form_picture):
    """
    method to save the picture
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

def save_audio(form_music):
    """
    method to save the audio
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_music.filename)
    music_fn = random_hex + f_ext
    music_path = os.path.join(app.root_path, 'static/music', music_fn)
    form_music.save(music_path)
    return music_fn
@app.route('/edit', methods=['GET', 'POST'])
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


def allowed_file(filename):
    """
    method to check if the file is allowed
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/handle_music', methods=['GET', 'POST'])
def handle_music():
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
            new_song = Music(title=request.form['title'], artist=request.form['artist'], duration=request.form['duration'], music_file=music_filename, picture=picture_filename)
            db.session.add(new_song)
            db.session.commit()
            flash("File Uploaded Successfully")
            return redirect('/handle_music')  # Redirect after successful upload

    return render_template('handle_music.html')
@app.route('/uploaded_music', methods=['GET'])
def uploaded_music():
    """
    method to upload music
    """
    musics = Music.query.all()
    return render_template('uploaded_music.html', musics=musics)
def send_mail(user):
    """
    method to send mail
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

# for podcast
def category_name():
    """retrieve the category name"""
    with get_db() as db:
        # query the db and get all the values from the name column
        category_names = db.query(Category.name).all()
        return category_names

def region_name():
    """retrieve the region name"""
    with get_db() as db:
        # query the region table and get all the values of the name column
        region_names = db.query(Region.name).all()
        return region_names

def country_name():
    """retrieve the country name"""
    with get_db() as db:
        country_names = db.query(Country.name).all()
        if not country_names:
            return None  # Or raise a specific exception like NotFound
        else:
            return country_names
 
def get_table_name():
    """retrieve the table name of the database"""
    with get_db() as db:
        table_names = inspect(db.get_bind()).get_table_names()
    return table_names

@app.route("/podcast/", methods=["GET", "POST"], strict_slashes=False)
def podcast():
    category_names = category_name()

    table_names = get_table_name()
    country_names = country_name()
    region_names = region_name()

    return render_template("podcast_page.html",  category_name=category_names,
                           table_name=table_names, country_name=country_names,
                           region_name=region_names)

@app.route('/old_music')
def old_music():
    """
    route for the music page
    """
    our_musics = Music.query.all()
    musics = get_music()
    return render_template('music.html', musics=musics, our_musics=our_musics)

@app.route('/account/music')
@login_required
def account_music():
    """
    route for the music page
    """
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    musics = get_music()
    return render_template('user_music.html', musics=musics, image_file=image_file)

@app.route('/artist/artist_id', methods=['GET'], strict_slashes=False)
def get_track(artist_id):
    key = os.environ.get('MY_API_KEY')
    if key is None:
        print("Error: API key not found in environment variables.")

    api_endpoint = f"https://api.musixmatch.com/ws/1.1/artist.get?artist_id={artist_id}&apikey={key}"
    headers = {"Authorization": f"Bearer {key}"}
    response = requests.get(api_endpoint, headers=headers)
    if response.status_code == 200:
        artist_info = response.json()
        # Process artist information
        print(artist_info)
    else:
        print("Error:", response.status_code)


@app.route('/playlists/create', methods=['GET', 'POST'], strict_slashes=False)
def create_playlists():
    """A method that creates and stores a playlist
    """
    form = CreatePlaylistForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.about.data
        image_url = form.image.data
        song_ids = form.songs.data

        playlists = playlist(
            title=title, description=description, image=image_url)

        # Associate selected songs with the playlist
        songs = Song.query.filter_by(
            id=song_ids).all()  # Get actual Song objects
        form.validate_songs(song_ids)
        playlist.songs.extend(songs)  # Add songs to the playlist relationship
        # return redirect('/playlist')
    # return render_template('/create_template')
    # return render_template()
