#! /usr/bin/python

from flask import Flask, render_template, url_for, request, g, Response, json
#import os.path
from flask.ext.assets import Bundle, Environment
from flask.ext.compress import Compress
import datetime
from pytz import timezone
import requests
import os



app = Flask(__name__)
app.config.from_pyfile('app.cfg')
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#app.config['REQUIREJS_BIN'] = os.path.dirname(__file__) + \
#    '/../node_modules/requirejs/bin/r.js'
#app.config['REQUIREJS_CONFIG'] = 'js/build.js'
app.config['REQUIREJS_RUN_IN_DEBUG'] = False

Compress(app)
assets = Environment(app)

def getFacebookAccess():
    url='https://graph.facebook.com/oauth/access_token?client_id={0}&client_secret={1}&grant_type=client_credentials'
    url = url.format(app.config['FACEBOOK_APPID'], app.config['FACEBOOK_APPSECRET'])
    resp = requests.get(url)
    access_token = resp.text.split('=')[1]
    return access_token

def scrapeFacebook(app_token):
    resp = requests.get("https://graph.facebook.com/v2.5/me?fields=id%2Cfirst_name%2Chometown%2Clocation%2Ctimezone%2Ctagged_places&debug=all&access_token="+app_token)
    s = resp.json()
    print s


@app.route('/')
def _index():
    access_token = getFacebookAccess()
    scrapeFacebook(app.config['FACEBOOK_APPID']+'|'+app.config['FACEBOOK_APPSECRET'])
    scrapeFacebook(access_token)
    return render_template('index.html', title = 'Callum\'s Travel Dashboard')


@app.route('/signup/', methods = [ 'GET', 'POST'])
def _signup():
    if request.method == 'GET':
        return render_template('signup.html')


@app.route('/login/', methods = ['GET', 'POST'])
def _login():
    if request.method == 'GET':
        return render_template('login.html',
                secret = str(os.urandom(12).encode('base64').replace('\n','')))
    elif request.method == 'POST':
        username = None
        password = None
        for key,value in request.values:
            if 'username' in key:
                username = request.values[key]
            elif 'password' in key:
                password = request.values[key]


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
