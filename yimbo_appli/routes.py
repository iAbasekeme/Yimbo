#!/usr/bin/python3
from flask import render_template, url_for, flash, redirect, session, request
from yimbo_appli import app, db, bcrypt, mail, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from yimbo_appli.forms import RegistrationForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm, UpdateAccountForm, HandleMusic
from yimbo_appli.models import User, Music
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
# for podcast
from yimbo_appli.model import Category, Region, Country, Podcast
from yimbo_appli.podcast_model import get_db
from sqlalchemy import inspect
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename


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

@app.route('/')
@app.route('/home')
def home_page():
    """
    route for the landing page define by wisdom
    """
    return  render_template('two_clone.html',  session=session.get('user'))
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
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        picture = request.files['picture']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            music_filename = secure_filename(file.filename)
            picture_filename = secure_filename(picture.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], music_filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], picture_filename))
            # add song to database
            new_song = Music(title=request.form['title'], artist=request.form['artist'], duration=request.form['duration'], music_file=music_filename, picture=picture_filename)
            db.session.add(new_song)
            db.session.commit()
            flash("File Uploaded Successfully")
        return render_template('handle_music.html')
            
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

@app.route('/music')
def music():
    """
    route for the music page
    """
    musics = get_music()
    return render_template('music.html', musics=musics)

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
