from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

import os
from dotenv import load_dotenv

# load the .env file that content secret information
load_dotenv()
UPLOAD_FOLDER = 'yimbo_appli/static/music'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'mp4', 'png', 'jpg', 'jpeg'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = '80ab528d4604e4d073b613216f6a0822'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///yimbo.db'

#app.register_blueprint(yb)
#app.register_blueprint(yb)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

# Login requierment
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# configure the mail sender
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
mail = Mail(app)

from yimbo_appli import routes

"""with app.app_context():
    db.create_all()"""
from yimbo_appli import routes


