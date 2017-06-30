#!/usr/bin python
# -*- coding: utf-8 -*-
'''
user.py handles user interactions like login, logout, ..
'''

from flask import render_template, redirect, request
from flask import session as login_session
from functions import createUser, getUserIdByMail
import random
import string

#GConnect
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

routes = []

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"


# USER helper-functions can be found in functions.py

def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for
                    x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)
routes.append(dict(
    rule='login/',
    view_func=showLogin))


def showLogout():
    try:
        provider = login_session['provider']
        if provider == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        # possibly add other providers here
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        return redirect('/')
    except:
        # maybe add flash messaging: 'you have not been logged in'
        print("logout went wrong, sorry")
        return redirect('/')
routes.append(dict(
    rule='logout/',
    view_func=showLogout))


def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    #stored_credentials = login_session.get('credentials')
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    #login_session['credentials'] = credentials
    login_session['provider'] = 'google'
    print("loginsession provider \n")
    print(login_session['provider'])
    print("\n provider ende \n")
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    print("\n===========USERNAME==========\"n")
    print(login_session['username'])
    print("\n===========USERNAME==========\"n")
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserIdByMail(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
        output = ''
        output += '<h1>Welcome back, '
        output += login_session['username']
        output += '!</h1>'
    else:
        output = ''
        output += '<h1>Welcome, '
        output += login_session['username']
        output += '!</h1>'
        output += '<img src="'
        output += login_session['picture']
        output += (' " style = "width: 300px; height: 300px;border-radius: '
                   '150px;-webkit-border-radius: 150px;-moz-border-radius: '
                   '150px;"> ')
        #flash("you are now logged in as %s" % login_session['username'])
        print("done!")
    login_session['user_id'] = user_id
    return output
routes.append(dict(
    rule='gconnect',
    view_func=gconnect,
    options=dict(methods=['POST'])))


def gdisconnect():
    if not login_session.get('access_token', None):
        return "not logged in"
    access_token = login_session['access_token']
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s') % (
        login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    # following is the same for logout for any provider, if add a new one just
    # move it into a extra function or prepend to showLogout()
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
