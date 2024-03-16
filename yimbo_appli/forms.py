#!/usr/bin/python3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from yimbo_appli.models import User


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
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')