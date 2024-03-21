from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .views import yb

app = Flask(__name__)

app.config['SECRET_KEY'] = '80ab528d4604e4d073b613216f6a0822'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///yimbo.db'

app.register_blueprint(yb)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from yimbo_appli import routes

with app.app_context():
    db.create_all()
