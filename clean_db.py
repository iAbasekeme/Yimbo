#!/bin/usr/python3
from yimbo_appli import app
from yimbo_appli import db
from yimbo_appli.models import User


with app.app_context():
    User.query.delete()
    db.session.commit()
    User.query.all()
