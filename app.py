#!/usr/bin/python3
"""
main route of the application
"""
from flask import Flask, render_template
app = Flask(__name__)


app.route('/home')
def home_page():
    """
    route for the landing page define by wisdom
    """
    return render_template('landin_page.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)