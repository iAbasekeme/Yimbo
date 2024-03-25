#!/usr/bin/python3
from flask import render_template, url_for, flash, redirect, session
from yimbo_appli import app, db, bcrypt
from yimbo_appli.forms import RegistrationForm, LoginForm
from yimbo_appli.models import User
from flask_login import login_user, current_user, logout_user
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
    """
    token = oauth.Yimbo.authorize_access_token()
    session['user'] = token
    return redirect(url_for('account')) 
    #return redirect(url_for("home_page"))

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
            #return redirect(url_for('home_page', user=user))
            return redirect(url_for('account', user=user))
            
        else:
            flash('Login Unsuccessful. Please check your email and your password', 'danger')
    return render_template('new_login.html',form=form)

@app.route('/account')
def account():
    return render_template('user.html')
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

@app.route('/music')
def music():
    """
    route for the music page
    """
    musics = get_music()
    return render_template('music.html', musics=musics)


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