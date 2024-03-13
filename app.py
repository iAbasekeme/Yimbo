#!/usr/bin/python3
"""
main route of the application
"""
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'
@app.route('/home')
def home_page():
    """
    route for the landing page define by wisdom
    """
    return render_template('home_page.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
