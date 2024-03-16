#!/usr/bin/python3
"""
main route of the application
"""
from yimbo_appli import app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
