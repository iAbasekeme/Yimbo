#!/usr/bin/python3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from yimbo_appli.models import User
from flask_login import current_user
from wtforms.fields import SelectMultipleField

# for importing file and validator
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
    """
    registration class for user registration
    it allow also to use some validation form
    """
    username = StringField('Username', validators= [DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        """
        function that check if the user already exist in the database.
        """
        
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. Please choose a different one.")

    def validate_email(self, email):
        """function that check if the user already exist in the database."""
        
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")
    

class LoginForm(FlaskForm):
    """
    login class for user to login 
    it allow also to use some validation form
    """
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
class ResetPasswordRequestForm(FlaskForm):
    """
    class for reset password request
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    
    def validate_email(self, email):
        """
        function that check if the user already exist in the database.
        """
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email. You must register first.")
        
class ResetPasswordForm(FlaskForm):
    """
    class for reset password
    """
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
    
    
class UpdateAccountForm(FlaskForm):
    """
    class for update account
    """
    username = StringField('Username', validators= [DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators= [DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Update')
    
    def validate_username(self, username):
        """
        function that check if the user already exist in the database.
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("That username is taken. Please choose a different one.")

    def validate_email(self, email):
        """
        function that check if the user already exist in the database.
        """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "That email is taken. Please choose a different one.")
class HandleMusic(FlaskForm):
    """
    class for handle music
    """
    title = StringField('Title', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    artist = StringField('Artist', validators=[DataRequired()])
    duration = StringField('Duration', validators=[DataRequired()])
    music = FileField('Upload Music', validators=[FileAllowed(['mp3'])])
    submit = SubmitField('Add')


class CreatePlaylistForm(FlaskForm):
    """
    A form form that creates a playlist
    """
    title = StringField('Title', validators=[DataRequired()])
    about = StringField('Description', validators=[DataRequired()])
    image = StringField('Image', validators=[DataRequired()])
    songs = SelectMultipleField(
        'Select songs', coerce=int, validators=[DataRequired()])

    def validate_songs(self, field):
        song_ids = field.data  # Get user-selected song IDs
        valid_songs = Song.query.filter_by(
            id=song_ids).all()  # Check if IDs exist
        if len(valid_songs) != len(song_ids):  # Check if all IDs are valid
            raise ValidationError(
                'Some selected songs are invalid or don\'t exist.')
