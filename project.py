#!/usr/bin python
# -*- coding: utf-8 -*-

from flask import Flask
app = Flask(__name__)

#generate a random string for the session to securely sign the cookie (CSRF)
from os import urandom

# import the routing
from modules import mod
app.register_blueprint(mod, url_prefix='/')


if __name__ == '__main__':
    app.secret_key = urandom(24)
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
