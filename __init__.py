#! /usr/bin/python
# -*- coding: utf-8 -*-

##MODULES
from flask import Flask, render_template, url_for, request, g, Response, json
from flask import redirect, flash, session
from flask.ext.assets import Bundle, Environment
from flask.ext.compress import Compress
import datetime
from pytz import timezone
import os
import psycopg2, psycopg2.extras

#CUSTOM
from functions import *
from myaccount import myAccount


app = Flask(__name__)
app.config.from_pyfile('app.cfg')
app.config['REQUIREJS_RUN_IN_DEBUG'] = False
app.register_blueprint(myAccount, url_prefix = '/myaccount')

Compress(app)
assets = Environment(app)


@app.before_request
def _beforeRequest():
    g.conn = psycopg2.connect(app.config['DB_CONN'],
            cursor_factory = psycopg2.extras.DictCursor)
    g.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    #because fuck everything about postgres's timezone handling.
    #Could maybe set this from the session .. ?
    g.conn.cursor().execute('''SET timezone = 'UTC';''')
    g.fb_token = getFacebookAccess()


@app.route('/')
def _index():
    return render_template('index.html', title = 'Callum\'s Journey',
            id = app.config['MASTER'])


@app.route('/signup/', methods = [ 'GET', 'POST'])
def _signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.values['username']
        password = request.values['password']
        email = request.values['email']
        fb_id, fb_token = None, None
        if 'token' in request.values:
            token = request.values['token']
            token = token.split('!')
            fb_token = token[0]
            fb_id = token[1]
            fb_expires = token[2]
            fb_signedrequest = token[3]
            qry = '''INSERT INTO facebook (id, access_token,expires_in,signed_request)
            VALUES ( %s, %s, %s, %s );'''
            try:
                query( qry, args = (fb_id, fb_token,fb_expires,fb_signedrequest))
            except psycopg2.IntegrityError as e:
                flash('That facebook account has already signed up.')
                return render_template('signup.html')

        fields = ['first_name','last_name', 'id', 'timezone']
        res = scrapeFacebook( fb_token if fb_token else g.fb_token, fb_id, fields )
        logging.debug( res )
        #locations = hometownLocation( res, g.fb_token )
        firstname = None
        surname = None
        timezone = None
        if res and isinstance(res,dict):
            firstname = res.get('first_name')
            surname = res.get('last_name')
            timezone = res.get('timezone')

        qry = '''INSERT INTO member ( url, fb_id, email, password, firstname,
        surname, current_tz ) VALUES ( %s, %s, %s, %s,%s,%s,%s ) RETURNING id;'''
        r = query( qry, args = ( username, fb_id, email, password, firstname,
        surname, timezone ), fetch_one = True )
        if r:
            session['id'] = r
            session['logged_in'] = True
            #updateHometownLocation( res, locations )
            return redirect( url_for('myAccount._index') )
        flash('An error Occurred, please try again later.')
        return render_template('signup.html')


@app.route('/logout/', methods = ['GET', 'POST'])
def _logout():
    for key in dict(session).keys():
        session.pop(key)
    flash('You\'ve been logged out.')
    return redirect(url_for('_login'))


@app.route('/login/', methods = ['GET', 'POST'])
def _login():
    if request.method == 'GET':
        return render_template('login.html',
                secret = str(os.urandom(12).encode('base64').replace('\n','')))
    elif request.method == 'POST':
        username = None
        password = None
        for key,value in request.values.iteritems():
            if 'username' in key:
                username = value
            elif 'password' in key:
                password = value

        qry = '''SELECT id, ( password = %s ) as logged_in FROM member WHERE
        url = %s'''
        r = query(qry, args = ( password, username ), fetch_row = True )
        if r:
            session['id'] = r['id']
            session['logged_in'] = r['logged_in']
            if session['logged_in']:
                return redirect( url_for('myAccount._index') )
            flash('Your password is incorrect.')
        else:
            flash('Your username or password is incorrect.')
        return render_template('login.html', secret =
            str(os.urandom(12).encode('base64').replace('\n','')))


@app.route('/getColour/')
def _getColour():
    return Response(json.dumps({ 'colour_1' : 'orange', 'colour_2' : 'purple'
        }), mimetype = 'Application/json')

@app.route('/timeSinceHome/')
def _timeSinceHome():
    left = datetime.datetime( day = 5, month = 8, year = 2015, hour = 11,
    minute = 0, second = 0, tzinfo = timezone('Pacific/Auckland'))
    epoch = datetime.datetime(1970,1,1).replace( tzinfo = timezone('Pacific/Auckland') )
    return Response( json.dumps({ 'startDate' : (left - epoch).total_seconds() }),
        mimetype = 'Application/json' )


if __name__ == '__main__':
    app.debug = app.config['DEBUG']
    app.run( '127.0.0.1', port = 8090 )
