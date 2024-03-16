#!/usr/bin/python3
from flask import render_template, url_for, flash, redirect
from yimbo_appli import app, db, bcrypt
from yimbo_appli.forms import RegistrationForm, LoginForm
from yimbo_appli.models import User
from flask_login import login_user, current_user
@app.route('/')
@app.route('/home')
def home_page():
    """
    route for the landing page define by wisdom
    """
    return render_template('main_page.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    method for registration
    
    if  current_user.is_authenticated:
        return  redirect(url_for('home_page'))"""
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
    
    if  current_user.is_authenticated:
        return  redirect(url_for('home_page'))"""
    form = LoginForm()
    if form.validate_on_submit():
        data = User.query.all()
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home_page'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('new_login.html',form=form)